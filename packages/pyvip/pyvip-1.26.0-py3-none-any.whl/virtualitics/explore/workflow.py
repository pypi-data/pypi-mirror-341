from typing import Union
import virtualitics.explore.workflow_entry as workflow_entry
import virtualitics.explore.workflow_constants as workflow_constants
import virtualitics.utils as utils

class Workflow (dict):
    def __init__(self):
        """Creates a Workflow object (:class:`dict`).

        Returns:
            :class:`Workflow`: Dictionary containing workflow entries.
        """
        base_dict = { workflow_constants.ENTRIES: [] }
        dict.__init__(self, base_dict)

    def __append_entry(self, entry: workflow_entry._WorkflowEntry):
        self[workflow_constants.ENTRIES].append(entry)

    def smart_mapping(self, task_description: str, target: str, features: list[str] = None, keep_missing_value_columns: bool = True) -> workflow_entry.SmartMappingEntry:
        """Creates and adds a Smart Mapping workflow entry.

        Args:
            task_description (:class:`str`): Display title of the entry.
            target (:class:`str`): Target column that the user wants to find insights about.
            features (:class:`list[str]`): List of column names that the user wants to analyze.
            keep_missing_value_columns (:class:`bool`): Whether to keep features with more than 50% missing values as part of the input. Default is `True`.

        Returns:
            :class:`workflow_entry.SmartMappingEntry`: Object containing all the parameters to run Smart Mapping.
        """

        sm_entry: workflow_entry.SmartMappingEntry = workflow_entry.SmartMappingEntry(task_description = task_description, target = target, features = features, keep_missing_value_columns = keep_missing_value_columns)

        self.__append_entry(sm_entry)

        return sm_entry
    
    def clustering(self, task_description: str, features: list[str] = None, num_clusters: int = None, keep_missing_value_columns: bool = True) -> workflow_entry.ClusteringEntry:
        """Creates and adds a Clustering workflow entry.

        Args:
            task_description (:class:`str`): Display title of the entry.
            features (:class:`list[str]`): List of column names that the user wants to analyze.
            num_clusters (:class:`None` | :class:`int`): between 2 and 16, specifying the number of clusters to compute. Default is `None` and enables 'auto'-mode where the number of clusters to compute is algorithmically determined based on stability.
            keep_missing_value_columns (:class:`bool`): Whether to keep features with more than 50% missing values as part of the input. Default is `True`.

        Returns:
            :class:`workflow_entry.ClusteringEntry`: Object containing all the parameters to run Clustering.
        """

        clustering_entry: workflow_entry.ClusteringEntry = workflow_entry.ClusteringEntry(task_description = task_description, features = features, num_clusters = num_clusters, keep_missing_value_columns = keep_missing_value_columns)

        self.__append_entry(clustering_entry)

        return clustering_entry
    
    def anomaly_detection(self, task_description: str, features: list[str] = None, plus_minus: str ="both", stdev: float = 0.5, and_or: str = "and", keep_missing_value_columns: bool = True) -> workflow_entry.AnomalyDetectionEntry:
        """Creates and adds an Anomaly Detection workflow entry.

        Args:
            task_description (:class:`str`): Display title of the entry.
            features (:class:`list[str]`): List of column names that the user wants to analyze.
            plus_minus (:class:`str`): Include outliers that are above, below, or above and below the desired standard deviation mark. Defaults to "both". Can be "both", "plus", or "minus".
            stdev (:class:`float`): User defined standard deviation on which to classify outliers. Default is 0.5.
            and_or (:class:`str`): "and" identifies data points that are outliers in all input features. "or" identifies data points that are outliers in any of the input features. Default is "and".
            keep_missing_value_columns (:class:`bool`): Whether to keep features with more than 50% missing values as part of the input. Default is `True`.

        Returns:
            :class:`workflow_entry.AnomalyDetectionEntry`: Object containing all the parameters to run Anomaly Detection.
        """

        ad_entry: workflow_entry.AnomalyDetectionEntry = workflow_entry.AnomalyDetectionEntry(task_description = task_description, features = features, plus_minus = plus_minus, stdev = stdev, and_or = and_or, keep_missing_value_columns = keep_missing_value_columns)

        self.__append_entry(ad_entry)

        return ad_entry
    
    def threshold_anomaly_detection(self, task_description: str, features: list[str] = None, threshold: float = 1, keep_missing_value_columns: bool = True) -> workflow_entry.ThresholdAnomalyDetectionEntry:
        """Creates and adds a Threshold Anomaly Detection workflow entry.

        Args:
            task_description (:class:`str`): Display title of the entry.
            features (:class:`list[str]`): List of column names that the user wants to analyze.
            threshold (:class:`float`): Percent threshold on which to classify outliers. Takes values from 0 to 100 exclusive. Defaults to a threshold of 1.
            keep_missing_value_columns (:class:`bool`): Whether to keep features with more than 50% missing values as part of the input. Default is `True`.

        Returns:
            :class:`workflow_entry.ThresholdAnomalyDetectionEntry`: Object containing all the parameters to run Threshold Anomaly Detection.
        """

        tad_entry: workflow_entry.ThresholdAnomalyDetectionEntry = workflow_entry.ThresholdAnomalyDetectionEntry(task_description = task_description, features = features, threshold = threshold, keep_missing_value_columns = keep_missing_value_columns)

        self.__append_entry(tad_entry)

        return tad_entry
    
    def pca(self, task_description: str, num_components: int, features: list[str] = None, keep_missing_value_columns: bool = True) -> workflow_entry.PCAEntry:
        """Creates and adds a PCA workflow entry.

        Args:
            task_description (:class:`str`): Display title of the entry.
            num_components (:class:`int`): Number of principle components to compute from the input data. The number of components must be within [1, 10] and cannot be greater than the number of features to run on.
            features (:class:`list[str]`): List of column names that the user wants to analyze.
            keep_missing_value_columns (:class:`bool`): Whether to keep features with more than 50% missing values as part of the input. Default is `True`.

        Returns:
            :class:`workflow_entry.PCAEntry`: Object containing all the parameters to run PCA.
        """

        pca_entry: workflow_entry.PCAEntry = workflow_entry.PCAEntry(task_description = task_description, num_components = num_components, features = features, keep_missing_value_columns = keep_missing_value_columns)

        self.__append_entry(pca_entry)

        return pca_entry
    
    def explainable_ai(self, task_description: str, xai_function: str, target: str, associative_columns: list[str] = None) -> workflow_entry.XAIEntry:
        """Creates and adds a XAI workflow entry.

        Args:
            task_description (:class:`str`): Display title of the entry.
            xai_function (:class:`str`): The type of explainability function to run. Can be "IdentificationTree", "RelativeEdgeDensity", "KolmogorovSmirnov".
            target (:class:`str`): Column that will be treated as the target categories for explainability.
            associative_columns (:class:`list[str]`): List of columns that will be used to as input alongside the target column.

        Returns:
            :class:`workflow_entry.XAIEntry`: Object containing all the parameters to run Explainable AI.
        """
        
        xai_entry: workflow_entry.XAIEntry = workflow_entry.XAIEntry(task_description = task_description, xai_function = xai_function, target = target, associative_columns = associative_columns)

        self.__append_entry(xai_entry)

        return xai_entry
    
    def network_extractor(self, task_description: str, node_column: str, associative_columns: list[str] = None, pivot_type: str = "mean", keep_missing_value_columns=True, extraction_type: str = "Categorical", standard_scale: bool = True, bypass_warning: bool = False) -> workflow_entry.NetworkExtractorEntry:
        """Creates and adds a Network Extractor workflow entry.

        Args:
            task_description (:class:`str`): Display title of the entry.
            node_column (:class:`str`): Column name containing values which will be treated as nodes in a network.
            associative_columns (:class:`list[str]`): List of column names that will be used to find associations between the nodes.
            pivot_type (:class:`str`) Specify the pivot type used to create aggregated columns in the resulting network dataset. Options are {"Min", "Max", "Mean", "Median", "Sum", "Std", "All"}. "Mean" is the default value.
            keep_missing_value_columns (:class:`bool`): Whether to keep features with more than 50% missing values as part of the input. Default is `True`.
            extraction_type (:class:`str`): Whether the extraction should be based on "Categorical" or "Numerical" associative features. Default is "Categorical".
            standard_scale (:class:`bool`): Whether to scale numerical values with respect to column mean and standard-deviation. Default is `True`.
            bypass_warning (:class:`bool`): Whether to bypass warning from Network Extractor tool that warns the user that the variety and size of the data will require large computational resources and memory. Use with care. Default is `False`.

        Returns:
            :class:`workflow_entry.NetworkExtractorEntry`: Object containing all the parameters to run Network Extractor.
        """

        pivot_type = utils.case_insensitive_match(utils.PIVOT_TYPES, pivot_type, "pivot_type")

        network_entry: workflow_entry.NetworkExtractorEntry = workflow_entry.NetworkExtractorEntry(task_description = task_description, node_column = node_column, associative_columns = associative_columns, pivot_type = pivot_type, keep_missing_value_columns = keep_missing_value_columns, extraction_type = extraction_type, standard_scale = standard_scale, bypass_warning = bypass_warning)

        self.__append_entry(network_entry)

        return network_entry
    
    def plot(self, task_description: str, plot_type: str, x: Union[str | None] = None, y: Union[str | None] = None, z: Union[str | None] = None, color: Union[str | None] = None, size: Union[str | None] = None,
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
                 trend_lines: Union[str | None] = None, scatter_plot_point_mode: Union[str | None] = None, line_plot_point_mode: Union[str | None] = None, edge_transparency: Union[float | None] = None, network_edge_mode: Union[str | None] = None) -> workflow_entry.PlotEntry:
        """Creates and adds a Plot workflow entry.

        Args:
            plot_type: {"scatter", "hist", "line", "maps3d", "maps2d", "ellipsoid", "surface", "convex_hull"}. Default is "scatter".
            x: X dimension.
            y: Y dimension.
            z: Z dimension.
            color: Color dimension. Automatically uses quartile/categorical coloring.
            size: Size dimension. Works best with continuous features.
            shape: Shape dimension. Works best with categorical features.
            transparency: Transparency dimension. Works best with continuous features.
            halo: Halo dimension. Works with binary features.
            halo_highlight: Optionally select a single value of the feature mapped to the Halo dimension. All points with this value will show a halo.
            pulsation: Pulsation dimension. Works best with categorical features.
            pulsation_highlight: Optionally select a single value of the feature mapped to the Pulsation dimension. All points with this value will pulsate.
            playback: Playback dimension. Requires user interaction to be activated; otherwise shows all.
            playback_highlight: Optionally select a single value of the feature mapped to the Playback dimension. All points with this value will be shown and all other points will be hidden.
            arrow: Arrow dimension. Works with continuous and categorical features.
            groupby: Group By dimension. Works with categorical columns.
            x_scale: Scaling factor for X dimension. Value must be between .5 and 10.
            y_scale: Scaling factor for Y dimension. Value must be between .5 and 10.
            z_scale: Scaling factor for Z dimension. Value must be between .5 and 10.
            x_range_min: Minimum visible value for the X dimension.
            x_range_max: Maximum visible value for the X dimension.
            x_limit_min: Minimum value displayed for the X dimension on the axis/grid box.
            x_limit_max: Maximum value displayed for the X dimension on the axis/grid box.
            x_limit_link: Whether limit is locked to range.
            y_range_min: Minimum visible value for the Y dimension.
            y_range_max: Maximum visible value for the Y dimension.
            y_limit_min: Minimum value displayed for the Y dimension on the axis/grid box.
            y_limit_max: Maximum value displayed for the Y dimension on the axis/grid box.
            y_limit_link: Whether limit is locked to range.
            z_range_min: Minimum visible value for the Z dimension.
            z_range_max: Maximum visible value for the Z dimension.
            z_limit_min: Minimum value displayed for the Z dimension on the axis/grid box.
            z_limit_max: Maximum value displayed for the Z dimension on the axis/grid box.
            z_limit_link: Whether limit is locked to range.
            size_scale: Scaling factor for Size dimension. Value must be between .5 and 10.
            transparency_scale: Scaling factor for Transparency dimension. Value must be between .5 and 10.
            halo_scale: Scaling factor for Halo dimension. Value must be between .5 and 10.
            arrow_scale: Scaling factor for Size dimension. Value must be between .5 and 10.
            color_type: User can select "gradient", "bin", or "palette" or None (which uses Virtualitics Explore defaults). For categorical data, the only option is color "palette". For numeric data, "bin" is the default but "gradient" can also be used.
            color_palette_id: User can select the color palette based on the available palettes for the specified color_type.
            color_inverted: :class:`bool` controlling the order of colors for all color types.
            color_normalization: Normalization setting for color. This can only be set if the color type is set to "Gradient". The options are "Log10", "Softmax", "IHST".
            x_normalization: Normalization setting for X. This can only be set if the feature mapped to this dimension is numerical and continuous. The options are "Log10", "Softmax", "IHST".
            y_normalization: Normalization setting for Y.This can only be set if the feature mapped to this dimension is numerical and continuous. The options are "Log10", "Softmax", "IHST".
            z_normalization: Normalization setting for Z. This can only be set if the feature mapped to this dimension is numerical and continuous. The options are "Log10", "Softmax", "IHST".
            size_normalization: Normalization setting for Size. This can only be set if the feature mapped to this dimension is numerical and continuous. The options are "Log10", "Softmax", "IHST".
            transparency_normalization: Normalization setting for Transparency.This can only be set if the feature mapped to this dimension is numerical and continuous. The options are "Log10", "Softmax", "IHST".
            arrow_normalization: Normalization setting for Arrow. This can only be set if the feature mapped to this dimension is numerical and continuous. The options are "Log10", "Softmax", "IHST".
            color_bins: sets the number of color bins to use. The max number of bins is 16. You must have at least as many unique values (in the column mapped to color) as the number of bins you set.
            color_bin_dist: :class:`str` with options: {"equal", "range"}.
            trend_lines: :class:`str` specifying whether to build trend lines for the plot, and how they should be broken down. Options: None, Color, GroupBy, All. Note: Trend lines are only available for scatter plot and line plot types.
            scatter_plot_point_mode: :class:`str` specifies whether to show or hide points in a scatter plot visualization. (Only valid for plot_type = 'scatter_plot')
            line_plot_point_mode: :class:`str` specifies whether to show or hide points and lines in a line plot visualization. (Only valid for plot_type = 'line_plot')
            viewby: :class:`str` specifies which viewby mode ("color" or "groupby") to use in a line plot visualization. (Only valid for plot_type = 'line_plot')
            show_points: Setting for how to view the confidence ellipsoids. Valid options are {True, False, "show", "hide"}.
            confidence: :class:`float` confidence probability that must be in {99.5, 99.0, 97.5, 95.0, 90.0, 80.0, 75.0, 70.0, 50.0, 30.0, 25.0, 20.0, 10.0, 5.0, 2.5, 1.0, 0.5}.
            map_provider: {"ArcGIS", "OpenStreetMap"} or `None`.
            map_style: depends on the map_provider. See documentation for options.
            globe_style: {"natural", "dark", "black ocean", "blue ocean", "gray ocean", "water color", "topographic", "moon", "night"}.
            lat_long_lines: :class:`bool` visibility setting for Latitude/Longitude lines.
            country_lines: :class:`bool` visibility setting for country border lines.
            heatmap_enabled: :class:`bool` setting for whether to use heatmap of the mapped data.
            heatmap_intensity: :class:`float` to determine the intensity of the heatmap. heatmap_enabled must be True for this parameter to be used.
            heatmap_radius: :class:`float` determining the radius of sensitivity for heatmap functionality.
            heatmap_enabled must be True for this parameter to be used.
            heatmap_radius_unit: determines the units of the heatmap_radius. Must be a :class:`str` and one of {"Kilometers", "Miles", "NauticalMiles"}. heatmap_enabled must be True for this parameter to be used.
            hist_volume_by: setting for metric used for height of histogram bins; {"count", "avg", "sum", "uniform"}.
            x_bins: :class:`int` between 1 and 1000 that sets the number of bins to use in the 'x' dimension.
            y_bins: :class:`int` between 1 and 1000 that sets the number of bins to use in the 'y' dimension.
            z_bins: :class:`int` between 1 and 1000 that sets the number of bins to use in the 'z' dimension.
            edge_transparency: Determines how transparent the edges will be. Fully transparent is 0 and fully opaque is 1.
            network_edge_mode: :class:`str`; Determines how many edges in the network will be rendered. Options are {"EdgeSample", "AllEdges", "HideEdges"}. EdgeSample is used if the value is not specified.

        Returns:
            :class:`workflow_entry.PlotEntry`: Object containing all the parameters to create a plot.
        """
        
        plot_entry: workflow_entry.PlotEntry = workflow_entry.PlotEntry(task_description = task_description, plot_type = plot_type, x = x, y = y, z = z, color = color, size = size, shape = shape, transparency = transparency, halo = halo, pulsation = pulsation,
                                                                        playback = playback, arrow = arrow, groupby = groupby, x_scale = x_scale, y_scale = y_scale, z_scale = z_scale,
                                                                        x_range_min = x_range_min, x_range_max = x_range_max, x_limit_min = x_limit_min, x_limit_max = x_limit_max, x_limit_link = x_limit_link, x_normalization = x_normalization,
                                                                        y_range_min = y_range_min, y_range_max = y_range_max, y_limit_min = y_limit_min, y_limit_max = y_limit_max, y_limit_link = y_limit_link, y_normalization = y_normalization,
                                                                        z_range_min = z_range_min, z_range_max = z_range_max, z_limit_min = z_limit_min, z_limit_max = z_limit_max, z_limit_link = z_limit_link, z_normalization = z_normalization,
                                                                        color_type = color_type, color_bins = color_bins, color_bin_dist = color_bin_dist, color_inverted = color_inverted, color_palette_id = color_palette_id,
                                                                        size_scale = size_scale, size_normalization = size_normalization,
                                                                        transparency_scale = transparency_scale, transparency_normalization = transparency_normalization,
                                                                        halo_scale = halo_scale, halo_highlight = halo_highlight,
                                                                        arrow_scale = arrow_scale, arrow_normalization = arrow_normalization,
                                                                        pulsation_highlight = pulsation_highlight, playback_higlight = playback_higlight,
                                                                        viewby = viewby, show_points = show_points, confidence = confidence, map_provider = map_provider, map_style = map_style,
                                                                        globe_style = globe_style, lat_long_lines = lat_long_lines, country_lines = country_lines, heatmap_enabled = heatmap_enabled, heatmap_intensity = heatmap_intensity,
                                                                        heatmap_radius = heatmap_radius, heatmap_radius_unit = heatmap_radius_unit, x_bins = x_bins, y_bins = y_bins, z_bins = z_bins, hist_volume_by = hist_volume_by,
                                                                        trend_lines = trend_lines, scatter_plot_point_mode = scatter_plot_point_mode, line_plot_point_mode = line_plot_point_mode, edge_transparency = edge_transparency, network_edge_mode = network_edge_mode)

        self.__append_entry(plot_entry)

        return plot_entry