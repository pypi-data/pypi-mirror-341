import os
import subprocess
import tempfile
from pathlib import Path
from typing import List

import numpy as np
import pandas as pd
import polars as pl
import polars.selectors as cs
import requests
import streamlit as st
from PIL import Image
from tensorboardX import SummaryWriter

from pixel_patrol.default_tabs import DefaultTabs
from pixel_patrol.utils.preprocessing import SPRITE_SIZE
from pixel_patrol.utils.utils import create_sprite_image
from pixel_patrol.widgets.widget_interface import ImagePrevalidationWidget


class EmbeddingProjectorWidget(ImagePrevalidationWidget):
    """
    This widget automatically selects numeric columns from your dataset
    and visualizes them as embeddings using TensorBoard’s Embedding Projector.
    """

    @property
    def tab(self) -> str:
        return DefaultTabs.VISUALIZATION.value

    @property
    def name(self) -> str:
        return "TensorBoard Embedding Projector"

    def required_columns(self) -> List[str]:
        """Returns required data column names"""
        return ["*"]


    def summary(self, data_frame: pl.DataFrame):
        df_numeric = data_frame.select(cs.by_dtype(pl.NUMERIC_DTYPES).replace(None, 0.0))
        st.write(f"✅ {df_numeric.shape[1]} numeric columns, "
                 f"with {df_numeric.shape[0]} rows can be utilized to display the data in the Embedding Projector.")


    def render(self, data_frame: pl.DataFrame):

        # Beginner-Friendly Introduction
        st.markdown("""
        The **Embedding Projector** allows you to explore high-dimensional data by reducing it to 
        2D or 3D using **Principal Component Analysis (PCA)** or **t-SNE**.

        **What is an embedding?**  
        - An embedding is a way to represent complex data (e.g., images, text) as points in a high-dimensional space.
        - The closer two points are, the more similar they are.

        **How does this tool help?**  
        - It helps visualize relationships between data points.
        - It enables exploration of clusters and patterns in large datasets.
        """)

        # Convert all columns to numeric, keeping only valid numeric ones
        df_numeric = data_frame.select(cs.by_dtype(pl.NUMERIC_DTYPES).replace(None, 0.0))
        df_metadata = data_frame.select(~cs.by_dtype(pl.NUMERIC_DTYPES) & ~cs.contains("thumbnail"))

        if df_numeric.is_empty():
            st.warning("No numeric data found! Embedding visualization requires numerical features.")
            return

        # Create embedding array
        embeddings_array = df_numeric.to_numpy()
        st.write(f"✅ Using {df_numeric.shape[1]} numeric columns, "
                 f"with {df_numeric.shape[0]} rows.")

        # Automatically Create a Temporary Directory
        temp_log_dir = Path(tempfile.mkdtemp())  # Uses a unique temp folder
        st.write(f"📂 Using temporary folder for TensorBoard logs: `{temp_log_dir}`")

        col1, col2, col3, col4, col5 = st.columns(5, vertical_alignment="bottom")

        with col1:
            # Launch TensorBoard
            port = st.number_input("📡 TensorBoard Port", value=6006, step=1)

        started = False
        stopped = False

        with col2:
            if st.button("🚀 Start TensorBoard"):
                st.session_state['tb_process'] = create_checkpoint_and_launch_tensorboard(temp_log_dir, data_frame, embeddings_array, port=port)
                started = True

        with col3:
            if started:
                st.markdown(f"[🔗 Open in new tab](http://127.0.0.1:{port}/#projector)")

        with col4:
            if st.button("🛑 Stop TensorBoard"):
                if "tb_process" in st.session_state:
                    st.session_state['tb_process'].terminate()
                    del st.session_state['tb_process']
                    stopped = True

        with col5:
            if started:
                st.success(f"TensorBoard is running on port {port}!")
            if stopped:
                st.success("TensorBoard stopped.")

        # Show the projector in an iframe
        if "tb_process" in st.session_state:
            st.markdown("### Embedding Projector UI")
            show_tensorboard_projector(port=port)


def generate_sprite_image_from_dataframe(df: pl.DataFrame, sprite_path="sprite.png"):
    """Creates a sprite image from thumbnails stored in a Polars DataFrame."""

    Path(sprite_path).parent.mkdir(parents=True, exist_ok=True)

    sprite_image = create_sprite_image(df)

    # Save sprite image
    sprite_image.save(sprite_path)
    print(f"✅ Sprite image saved: {sprite_path}")


def generate_projector_checkpoint(
        embeddings: np.ndarray,
        meta_df: pd.DataFrame,
        log_dir: Path,
):
    """Creates TensorBoard embedding files without TensorFlow dependency."""

    # Load sprite image as numpy array
    sprite_image = None
    if "thumbnail" in meta_df.columns:
        sprite_image = np.array(meta_df["thumbnail"].to_list())
        sprite_image = [(np.array(img) - np.min(img)) / (np.max(img) - np.min(img)) for img in sprite_image]
        sprite_image = np.array([Image.fromarray(img.astype(float)).resize((SPRITE_SIZE, SPRITE_SIZE)) for img in sprite_image])
        # Add channel dimension if images are single-channel
        if len(sprite_image.shape) == 3:  # (N, H, W) - no channel dimension
            sprite_image = np.expand_dims(sprite_image, axis=1)  # becomes (N, H, W, 1)

    # Extract metadata columns
    # FIXME still converting to pandas here
    df_labels = meta_df.clone().drop("thumbnail").to_pandas()

    # Sanitize tabs in metadata content (prevents accidental column splits)
    sanitized_df = df_labels.astype(str).replace(r'\t', ' ', regex=True)

    # Convert to list of lists (each row is a list of column values)
    metadata = sanitized_df.values.tolist()

    # Write embeddings with tensorboardX
    with SummaryWriter(logdir=str(log_dir)) as writer:
        writer.add_embedding(
            mat=embeddings,
            metadata=metadata,
            metadata_header=sanitized_df.columns.to_list(),
            label_img=sprite_image,
            tag="my_embedding",
            global_step=0
        )

def create_checkpoint_and_launch_tensorboard(temp_log_dir, data_frame: pl.DataFrame, embeddings_array, port: int = 6006):
    """Launch TensorBoard as a subprocess."""
    generate_projector_checkpoint(embeddings_array, data_frame, temp_log_dir)

    return launch_tensorboard(temp_log_dir, port)


def launch_tensorboard(logdir, port):
    cmd = ["tensorboard", f"--logdir={logdir}", f"--port={port}", "--bind_all"]
    env = os.environ.copy()
    env["GCS_READ_CACHE_MAX_SIZE_MB"] = "0"
    tb_process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=env)
    import time
    for _ in range(50):
        try:
            r = requests.get(f"http://127.0.0.1:{port}")
            if r.status_code == 200:
                break
        except requests.exceptions.ConnectionError:
            pass
        time.sleep(0.2)
    return tb_process


def show_tensorboard_projector(port: int):
    """Embed TensorBoard's projector in Streamlit."""
    tb_url = f"http://127.0.0.1:{port}/#projector"
    st.components.v1.iframe(tb_url, height=800, scrolling=True)
