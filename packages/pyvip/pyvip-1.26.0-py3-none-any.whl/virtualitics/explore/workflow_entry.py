from typing import Union
import virtualitics.explore.workflow_constants as workflow_constants
import virtualitics.utils as utils

class _WorkflowEntry(dict):
    def __init__(self, task_description: str, entryData: dict):

        base_dict = {
                workflow_constants.TASK_DESCRIPTION: task_description,
                workflow_constants.EVENT_TYPE: workflow_constants.TASK.upper(),
                workflow_constants.TASK: entryData
            }

        dict.__init__(self, base_dict)
    
class SmartMappingEntry (_WorkflowEntry):
    def __init__(self, task_description: str, target: str, features: list[str] = None, keep_missing_value_columns: bool = True):

        sm_dict = {
            workflow_constants.TASK_TYPE: workflow_constants.SMART_MAPPING,
            workflow_constants.TARGET: target,
            workflow_constants.KEEP_MV: keep_missing_value_columns,
            workflow_constants.FEATURES: features
        }

        super().__init__(task_description, sm_dict)

class ClusteringEntry (_WorkflowEntry):
    def __init__(self, task_description: str, features: list[str] = None, num_clusters: int = None, keep_missing_value_columns: bool = True):

        clustering_dict = {
            workflow_constants.TASK_TYPE: workflow_constants.CLUSTERING,
            workflow_constants.NUMBER_CLUSTERS: num_clusters,
            workflow_constants.KEEP_MV: keep_missing_value_columns,
            workflow_constants.APPLY: True, # This parameter is deprecated in api.py. We auto apply it for the user.
            workflow_constants.FEATURES: features
        }

        super().__init__(task_description, clustering_dict)

class AnomalyDetectionEntry (_WorkflowEntry):
    def __init__(self, task_description: str, features: list[str] = None, plus_minus: str ="both", stdev: float = 0.5, and_or: str = "and", keep_missing_value_columns: bool = True):

        and_or: bool = utils.case_insensitive_match(utils.AND_OR_CHOICES, and_or, "and_or") if and_or is not None else None
        plus_minus: int = utils.case_insensitive_match(utils.POS_NEG_CHOICES, plus_minus, "plus_minus") if plus_minus is not None else None

        ad_dict = {
            workflow_constants.TASK_TYPE: workflow_constants.ANOMALY_DETECTION,
            workflow_constants.POSITIVE_NEGATIVE: plus_minus,
            workflow_constants.STD_DEV: stdev,
            workflow_constants.AND_OR: and_or,
            workflow_constants.APPLY: True, # This parameter is deprecated in api.py. We auto apply it for the user.
            workflow_constants.KEEP_MV: keep_missing_value_columns,
            workflow_constants.FEATURES: features
        }

        super().__init__(task_description, ad_dict)

class ThresholdAnomalyDetectionEntry (_WorkflowEntry):
    def __init__(self, task_description: str, features: list[str] = None, threshold: float = 1, keep_missing_value_columns: bool = True):

        ad_dict = {
            workflow_constants.TASK_TYPE: workflow_constants.PCA_ANOMALY_DETECTION,
            workflow_constants.THRESHOLD: threshold,
            workflow_constants.APPLY: True, # This parameter is deprecated in api.py. We auto apply it for the user.
            workflow_constants.KEEP_MV: keep_missing_value_columns,
            workflow_constants.FEATURES: features
        }

        super().__init__(task_description, ad_dict)

class PCAEntry (_WorkflowEntry):
    def __init__(self, task_description: str, num_components: int, features: list[str] = None, keep_missing_value_columns: bool = True):

        pca_dict = {
            workflow_constants.TASK_TYPE: workflow_constants.PCA,
            workflow_constants.NUMBER_COMPONENTS: num_components,
            workflow_constants.KEEP_MV: keep_missing_value_columns,
            workflow_constants.APPLY: True, # This parameter is deprecated in api.py. We auto apply it for the user.
            workflow_constants.FEATURES: features
        }
        
        super().__init__(task_description, pca_dict)

class XAIEntry (_WorkflowEntry):
    def __init__(self, task_description: str, xai_function: str, target: str, associative_columns: list[str] = None):
        
        xai_dict = {
            workflow_constants.TASK_TYPE: workflow_constants.XAI,
            workflow_constants.TARGET_FEATURE: target, # For some reason XAI was setup to use "Target Feature" instead of "Feature".
            workflow_constants.XAI_FUNCTION: xai_function,
            workflow_constants.ASSOCIATIVE_FEATURES: associative_columns
        }

        super().__init__(task_description, xai_dict)

class NetworkExtractorEntry (_WorkflowEntry):
    def __init__(self, task_description: str, node_column: str, associative_columns: list[str] = None, pivot_type: str = "mean", keep_missing_value_columns=True, extraction_type: str = "Categorical", standard_scale: bool = True, bypass_warning: bool = False):

        pivot_type: str = utils.case_insensitive_match(utils.PIVOT_TYPES, pivot_type, "pivot_type") if pivot_type is not None else None

        network_dict = {
            workflow_constants.TASK_TYPE: workflow_constants.NETWORK_EXTRACTOR,
            workflow_constants.NODE_COLUMN: node_column,
            workflow_constants.PIVOT_TYPE: pivot_type,
            workflow_constants.KEEP_MV: keep_missing_value_columns,
            workflow_constants.EXTRACTION_TYPE: extraction_type,
            workflow_constants.ASSOCIATIVE_COLUMNS: associative_columns,
            workflow_constants.STANDARD_SCALE: standard_scale,
            workflow_constants.BYPASS_WARNING: bypass_warning
        }

        super().__init__(task_description, network_dict)

class PlotEntry (_WorkflowEntry):
    def __init__(self, task_description: str, plot_type: str, x: Union[str | None] = None, y: Union[str | None] = None, z: Union[str | None] = None, color: Union[str | None] = None, size: Union[str | None] = None,
                 shape: Union[str | None] = None, transparency: Union[str | None] = None, halo: Union[str | None] = None, pulsation: Union[str | None] = None, playback: Union[str | None] = None, arrow: Union[str | None] = None,
                 groupby: Union[str | None] = None, x_scale: Union[float | None] = None, y_scale: Union[float | None] = None, z_scale: Union[float | None] = None,
                 x_range_min: Union[float | None] = None, x_range_max: Union[float | None] = None, x_limit_min: Union[float | None] = None, x_limit_max: Union[float | None] = None, x_limit_link: Union[bool | None] = None, x_normalization: Union[str | None] = None,
                 y_range_min: Union[float | None] = None, y_range_max: Union[float | None] = None, y_limit_min: Union[float | None] = None, y_limit_max: Union[float | None] = None, y_limit_link: Union[bool | None] = None, y_normalization: Union[str | None] = None,
                 z_range_min: Union[float | None] = None, z_range_max: Union[float | None] = None, z_limit_min: Union[float | None] = None, z_limit_max: Union[float | None] = None, z_limit_link: Union[bool | None] = None, z_normalization: Union[str | None] = None,
                 color_type: Union[str | None] = None, color_bins: Union[str | None] = None, color_bin_dist: Union[str | None] = None, color_inverted: Union[str | None] = None, color_palette_id: Union[str | None] = None,
                 size_scale: Union[float | None] = None, size_normalization: Union[str | None] = None,
                 transparency_scale: Union[float | None] = None, transparency_normalization: Union[str | None] = None,
                 halo_scale: Union[float | None] = None, halo_highlight: Union[str | None] = None,
                 arrow_scale: Union[float | None] = None, arrow_normalization: Union[str | None] = None,
                 pulsation_highlight: Union[str | None] = None, playback_higlight: Union[str | None] = None,
                 viewby: Union[str | None] = None, show_points: Union[bool | None] = None, confidence: Union[float | None] = None, map_provider: Union[str | None] = None, map_style: Union[str | None] = None,
                 globe_style: Union[str | None] = None, lat_long_lines: Union[str | bool | None] = None, country_lines: Union[str | bool | None] = None, heatmap_enabled: Union[bool | None] = None, heatmap_intensity: Union[float | None] = None,
                 heatmap_radius: Union [float | None] = None, heatmap_radius_unit: Union [float | None] = None, x_bins: Union [int | None] = None, y_bins: Union [int | None] = None, z_bins: Union [int | None] = None, hist_volume_by: Union [int | None] = None,
                 trend_lines: Union[str | None] = None, scatter_plot_point_mode: Union[str | None] = None, line_plot_point_mode: Union[str | None] = None, edge_transparency: Union[float | None] = None, network_edge_mode: Union[str | None] = None):
        
        plot_type: str = utils.case_insensitive_match(utils.PLOT_TYPE_ALIASES, plot_type, "plot_type") if plot_type is not None else None
        color_type: str = utils.case_insensitive_match(utils.COLOR_OPTIONS, color_type, "color_type") if color_type is not None else None
        color_bin_dist: str = utils.case_insensitive_match(utils.COLOR_BIN_MODES, color_bins, "color_bin_dist") if color_bins is not None else None
        x_normalization: str = utils.case_insensitive_match(utils.NORMALIZATION_OPTIONS, x_normalization, "x_normalization") if x_normalization is not None else None
        y_normalization: str = utils.case_insensitive_match(utils.NORMALIZATION_OPTIONS, y_normalization, "y_normalization") if y_normalization is not None else None
        z_normalization: str = utils.case_insensitive_match(utils.NORMALIZATION_OPTIONS, z_normalization, "z_normalization") if z_normalization is not None else None
        size_normalization: str = utils.case_insensitive_match(utils.NORMALIZATION_OPTIONS, size_normalization, "size_normalization") if size_normalization is not None else None
        transparency_normalization: str = utils.case_insensitive_match(utils.NORMALIZATION_OPTIONS, transparency_normalization, "transparency_normalization") if transparency_normalization is not None else None
        arrow_normalization: str = utils.case_insensitive_match(utils.NORMALIZATION_OPTIONS, arrow_normalization, "arrow_normalization") if arrow_normalization is not None else None
        confidence: str = utils.case_insensitive_match(utils.CONFIDENCE_LEVELS, confidence, "confidence") if confidence is not None else None
        globe_style: int = utils.case_insensitive_match(utils.GLOBE_STYLE_OPTIONS, globe_style, "globe_style") if globe_style is not None else None
        map_provider: int = utils.case_insensitive_match(utils.MAP_PROVIDERS, map_provider, "map_provider") if map_provider is not None else None
        map_style = utils.case_insensitive_match(utils.MAP_STYLES[map_provider], map_style, "map_style") if map_style is not None and map_provider is not None else None
        hist_volume_by: str = utils.case_insensitive_match(utils.VOLUME_BY_MODES, hist_volume_by, "hist_volume_by") if hist_volume_by is not None else None
        heatmap_radius_unit: str = utils.case_insensitive_match(utils.HEATMAP_RADIUS_UNITS, heatmap_radius_unit, "heatmap_radius_unit") if heatmap_radius_unit is not None else None
        viewby: str = utils.case_insensitive_match(utils.VIEWBY_MODES, viewby, "viewby") if viewby is not None else None

        # Dimensions/Column Names.
        mapped_dimensions_dict = [
            { workflow_constants.DIMENSION: workflow_constants.DIM_X, workflow_constants.COLUMN: x },
            { workflow_constants.DIMENSION: workflow_constants.DIM_Y, workflow_constants.COLUMN: y },
            { workflow_constants.DIMENSION: workflow_constants.DIM_Z, workflow_constants.COLUMN: z },
            { workflow_constants.DIMENSION: workflow_constants.DIM_COLOR, workflow_constants.COLUMN: color },
            { workflow_constants.DIMENSION: workflow_constants.DIM_SIZE, workflow_constants.COLUMN: size },
            { workflow_constants.DIMENSION: workflow_constants.DIM_SHAPE, workflow_constants.COLUMN: shape },
            { workflow_constants.DIMENSION: workflow_constants.DIM_TRANSPARENCY, workflow_constants.COLUMN: transparency },
            { workflow_constants.DIMENSION: workflow_constants.DIM_HALO, workflow_constants.COLUMN: halo },
            { workflow_constants.DIMENSION: workflow_constants.DIM_PULSATION, workflow_constants.COLUMN: pulsation },
            { workflow_constants.DIMENSION: workflow_constants.DIM_PLAYBACK, workflow_constants.COLUMN: playback },
            { workflow_constants.DIMENSION: workflow_constants.DIM_ARROW, workflow_constants.COLUMN: arrow },
            { workflow_constants.DIMENSION: workflow_constants.DIM_GROUP_BY, workflow_constants.COLUMN: groupby }
        ]

        plot_settings_dict = {
            # Dimension X.
            workflow_constants.DIM_X_SCALE: x_scale,
            workflow_constants.DIM_X_RANGE_MIN: x_range_min,
            workflow_constants.DIM_X_RANGE_MAX: x_range_max,
            workflow_constants.DIM_X_LIMIT_MIN: x_limit_min,
            workflow_constants.DIM_X_LIMIT_MAX: x_limit_max,
            workflow_constants.DIM_X_LIMIT_LINK: x_limit_link,
            workflow_constants.DIM_X_NORM: x_normalization,

            # Dimension Y.
            workflow_constants.DIM_Y_SCALE: y_scale,
            workflow_constants.DIM_Y_RANGE_MIN: y_range_min,
            workflow_constants.DIM_Y_RANGE_MAX: y_range_max,
            workflow_constants.DIM_Y_LIMIT_MIN: y_limit_min,
            workflow_constants.DIM_Y_LIMIT_MAX: y_limit_max,
            workflow_constants.DIM_Y_LIMIT_LINK: y_limit_link,
            workflow_constants.DIM_Y_NORM: y_normalization,

            # Dimension Z.
            workflow_constants.DIM_Z_SCALE: z_scale,
            workflow_constants.DIM_Z_RANGE_MIN: z_range_min,
            workflow_constants.DIM_Z_RANGE_MAX: z_range_max,
            workflow_constants.DIM_Z_LIMIT_MIN: z_limit_min,
            workflow_constants.DIM_Z_LIMIT_MAX: z_limit_max,
            workflow_constants.DIM_Z_LIMIT_LINK: z_limit_link,
            workflow_constants.DIM_Z_NORM: z_normalization,

            # Dimension Color.
            workflow_constants.DIM_COLOR_TYPE: color_type,
            workflow_constants.DIM_COLOR_BINS: color_bins,
            workflow_constants.DIM_COLOR_BINS_DST: color_bin_dist,
            workflow_constants.DIM_COLOR_INVERTED: color_inverted,
            workflow_constants.DIM_COLOR_PALETTE_ID: color_palette_id,

            # Dimension Size.
            workflow_constants.DIM_SIZE_SCALE: size_scale,
            workflow_constants.DIM_SIZE_NORMALIZATION: size_normalization,

            # Dimension Transparency.
            workflow_constants.DIM_TRANSPARENCY_SCALE: transparency_scale,
            workflow_constants.DIM_TRANSPARENCY_NORMALIZATION: transparency_normalization,

            # Dimension Halo.
            workflow_constants.DIM_HALO_SCALE: halo_scale,
            workflow_constants.DIM_HALO_HIGHLIGHT: halo_highlight,

            # Dimension Arrow.
            workflow_constants.DIM_ARROW_SCALE: arrow_scale,
            workflow_constants.DIM_ARROW_NORMALIZATION: arrow_normalization,

            # Dimension Pulsation.
            workflow_constants.DIM_PULSATION_HIGHLIGHT: pulsation_highlight,

            # Dimension Playback.
            workflow_constants.DIM_PLAYBACK_HIGHLIGHT: playback_higlight,

            # Plot Settings.
            workflow_constants.VIEW_BY: viewby,
            workflow_constants.SHOW_POINTS: show_points,
            workflow_constants.CONFIDENCE: confidence,
            workflow_constants.MAP_PROVIDER: map_provider,
            workflow_constants.MAP_STYLE: map_style,
            workflow_constants.GLOBE_STYLE: globe_style,
            workflow_constants.LAT_LONG_LINES: lat_long_lines,
            workflow_constants.COUNTRY_LINES: country_lines,
            workflow_constants.HEATMAP_ENABLED: heatmap_enabled,
            workflow_constants.HEATMAP_INTENSITY: heatmap_intensity,
            workflow_constants.HEATMAP_RADIUS: heatmap_radius,
            workflow_constants.HEATMAP_RADIUS_UNIT: heatmap_radius_unit,
            workflow_constants.X_BINS: x_bins,
            workflow_constants.Y_BINS: y_bins,
            workflow_constants.Z_BINS: z_bins,
            workflow_constants.HIST_VOLUMN_BY: hist_volume_by,
            workflow_constants.TREND_LINES: trend_lines,
            workflow_constants.POINT_MODE: scatter_plot_point_mode,
            workflow_constants.LINE_PLOT_POINT_MODE: line_plot_point_mode,
            workflow_constants.EDGE_TRANSPARENCY: edge_transparency,
            workflow_constants.NETWORK_EDGE_MODE: network_edge_mode
        }
        
        plot_dict = {
            workflow_constants.TASK_TYPE: workflow_constants.PLOT,
            workflow_constants.PLOT_TYPE: plot_type,

            workflow_constants.DIMENSION_INFO: mapped_dimensions_dict,
            workflow_constants.PLOT_SETINGS: plot_settings_dict
        }

        super().__init__(task_description, plot_dict)