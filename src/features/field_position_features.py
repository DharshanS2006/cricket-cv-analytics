import pandas as pd
import os


CSV_PATH = "data/processed/tracking/player_tracks.csv"
OUTPUT_PATH = "data/processed/features/field_position_features.csv"


def get_region(x_normalized, y_normalized):
    """
    Divide the image into a 3x3 grid.

    This is image-space analysis only.
    It is not yet a real cricket-field position.
    """

    if y_normalized < 1 / 3:
        vertical = "top"
    elif y_normalized < 2 / 3:
        vertical = "middle"
    else:
        vertical = "bottom"

    if x_normalized < 1 / 3:
        horizontal = "left"
    elif x_normalized < 2 / 3:
        horizontal = "center"
    else:
        horizontal = "right"

    return f"{vertical}_{horizontal}"


def calculate_field_position_features():

    print("=" * 45)
    print("       FIELD POSITION FEATURES")
    print("=" * 45)

    print(f"Loading : {CSV_PATH}")

    df = pd.read_csv(CSV_PATH)

    print(f"Total detections : {len(df)}")
    print(f"Unique IDs       : {df['track_id'].nunique()}")

    # Get video dimensions from tracking coordinates
    video_width = df["x2"].max()
    video_height = df["y2"].max()

    print(f"Estimated width  : {video_width:.0f}")
    print(f"Estimated height : {video_height:.0f}")

    results = []

    for track_id, player in df.groupby("track_id"):

        player = player.sort_values("frame")

        x = player["center_x"]
        y = player["center_y"]

        avg_x = x.mean()
        avg_y = y.mean()

        min_x = x.min()
        max_x = x.max()
        min_y = y.min()
        max_y = y.max()

        position_spread_x = max_x - min_x
        position_spread_y = max_y - min_y

        # Normalize coordinates between 0 and 1
        avg_x_normalized = avg_x / video_width
        avg_y_normalized = avg_y / video_height

        dominant_region = get_region(
            avg_x_normalized,
            avg_y_normalized
        )

        movement_area = (
            position_spread_x *
            position_spread_y
        )

        results.append({
            "track_id": int(track_id),
            "detections": len(player),

            "average_x": round(avg_x, 2),
            "average_y": round(avg_y, 2),

            "minimum_x": round(min_x, 2),
            "maximum_x": round(max_x, 2),

            "minimum_y": round(min_y, 2),
            "maximum_y": round(max_y, 2),

            "position_spread_x": round(position_spread_x, 2),
            "position_spread_y": round(position_spread_y, 2),

            "movement_area_pixels": round(
                movement_area,
                2
            ),

            "average_x_normalized": round(
                avg_x_normalized,
                4
            ),

            "average_y_normalized": round(
                avg_y_normalized,
                4
            ),

            "dominant_region": dominant_region
        })

    results_df = pd.DataFrame(results)

    results_df = results_df.sort_values(
        "detections",
        ascending=False
    )

    os.makedirs(
        "data/processed/features",
        exist_ok=True
    )

    results_df.to_csv(
        OUTPUT_PATH,
        index=False
    )

    print()
    print("Field position analysis complete.")
    print()

    print(
        results_df.head(10).to_string(
            index=False
        )
    )

    print()
    print("=" * 45)
    print("OUTPUT")
    print("=" * 45)
    print(f"Saved : {OUTPUT_PATH}")
    print("=" * 45)


if __name__ == "__main__":
    calculate_field_position_features()