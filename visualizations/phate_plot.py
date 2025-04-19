import pandas as pd
import phate
import plotly.express as px
import numpy as np

def main():
    print("📂 Loading processed data...")
    df = pd.read_pickle("../data/data.pkl")

    print("📊 Extracting SBERT embeddings...")
    embeddings = np.vstack(df["embedding"].values)

    # Remove duplicate embeddings
    print("🧹 Removing duplicate embeddings...")
    _, unique_indices = np.unique(embeddings, axis=0, return_index=True)
    embeddings = embeddings[sorted(unique_indices)]
    df = df.iloc[sorted(unique_indices)].reset_index(drop=True)

    # Ensure topic labels are cleaned
    df["topic_label"] = df["topic_label"].astype(str).str.strip()

    # ---------- 2D PHATE ----------
    print("🔄 Running 2D PHATE...")
    phate_2d = phate.PHATE(n_components=2, n_jobs=-1)
    phate_embedding_2d = phate_2d.fit_transform(embeddings)

    df["PHATE1"] = phate_embedding_2d[:, 0]
    df["PHATE2"] = phate_embedding_2d[:, 1]

    print("📈 Plotting 2D PHATE...")
    fig_2d = px.scatter(
        df,
        x="PHATE1",
        y="PHATE2",
        color="topic_label",
        hover_data=["processed_comment"],
        title="2D PHATE Visualization of SBERT Embeddings",
        width=1200,
        height=800,
    )
    fig_2d.write_html("phate_2d_plot.html")
    print("✅ Saved 2D PHATE plot to 'phate_2d_plot.html'")

    # ---------- 3D PHATE ----------
    print("🔄 Running 3D PHATE...")
    phate_3d = phate.PHATE(n_components=3, n_jobs=-1)
    phate_embedding_3d = phate_3d.fit_transform(embeddings)

    df["PHATE1"] = phate_embedding_3d[:, 0]
    df["PHATE2"] = phate_embedding_3d[:, 1]
    df["PHATE3"] = phate_embedding_3d[:, 2]

    print("📈 Plotting 3D PHATE...")
    fig_3d = px.scatter_3d(
        df,
        x="PHATE1",
        y="PHATE2",
        z="PHATE3",
        color="topic_label",
        hover_data=["processed_comment"],
        title="3D PHATE Visualization of SBERT Embeddings",
        width=1200,
        height=800,
    )
    fig_3d.update_layout(
        scene_camera=dict(eye=dict(x=1.5, y=1.5, z=1.2)),
        showlegend=True
    )
    fig_3d.write_html("phate_3d_plot.html")
    print("✅ Saved 3D PHATE plot to 'phate_3d_plot.html'")

if __name__ == "__main__":
    main()