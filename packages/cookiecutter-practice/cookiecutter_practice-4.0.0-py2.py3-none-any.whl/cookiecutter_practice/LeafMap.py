import ipyleaflet
import logging
import geopandas as gpd


class Map(ipyleaflet.Map):
    __layer_control = None
    __layers = {}

    def __init__(self, center=(20, 0), zoom=2, height="600px", **kwargs):
        """Create a LeafMap Map instance.

        Params:
            center (tuple): The center of the map (latitude, longitude)
            zoom (int): The initial zoom level of the map
            height (str): The height of the map
            **kwargs: Additional keyword arguments

        """
        super().__init__(center=center, zoom=zoom, scroll_wheel_zoom=True, **kwargs)
        self.layout.height = height

    def add_basemap(self, basemap="OpenTopoMap"):
        """Add a basemap/layer to the map.

        Params:
            basemap (str): The name of the basemap/layer to add. Can be one of the following: 'OpenStreetMap.Mapnik', 'OpenStreetMap.BlackAndWhite', 'OpenStreetMap.DE', 'OpenStreetMap.France', 'OpenStreetMap.HOT', 'OpenStreetMap.Mapnik', 'OpenStreetMap.CH', 'OpenStreetMap.BZH', 'OpenStreetMap.Land', 'OpenStreetMap.HYB', 'OpenStreetMap.OSM

        Returns:
            None

        """
        try:
            url = eval(f"ipyleaflet.basemaps.{basemap}").build_url()
            layer = ipyleaflet.TileLayer(name=basemap, url=url)
            self.__layers[basemap] = layer
            self.add(item=layer)
        except AttributeError:
            logging.warning(f"Basemap {basemap} not found. Using OpenTopoMap instead.")
            layer = ipyleaflet.TileLayer(
                name=ipyleaflet.basemaps.OpenTopoMap.name,
                url=ipyleaflet.basemaps.OpenTopoMap.build_url(),
            )
            self.__layers[ipyleaflet.basemaps.OpenTopoMap.name] = layer
            self.add(layer)

    def remove_basemap(self, basemap):
        """Remove a basemap/layer from the map.

        Params:
            basemap (str): The name of the basemap/layer to remove. Can be one of the following: 'OpenStreetMap.Mapnik', 'OpenStreetMap.BlackAndWhite', 'OpenStreetMap.DE', 'OpenStreetMap.France', 'OpenStreetMap.HOT', 'OpenStreetMap.Mapnik', 'OpenStreetMap.CH', 'OpenStreetMap.BZH', 'OpenStreetMap.Land', 'OpenStreetMap.HYB', 'OpenStreetMap.OSM

        Returns:
            bool: True if the basemap/layer was removed, False otherwise

        """
        try:
            if basemap in self.__layers:
                self.remove(self.__layers[basemap])
                self.__layers.pop(basemap)
                return True
            else:
                logging.warning(f"Basemap/layer {basemap} not found.")
                return False
        except AttributeError:
            logging.warning(f"There was an error removing the basemap/layer {basemap}.")
            return False

    def add_layer_control(self, position="topright"):
        """Add a layer control to the map.

        Params:
            position (str): The position of the control (one of the map corners), can be 'topleft', 'topright', 'bottomleft' or 'bottomright'

        """
        if position not in ["topleft", "topright", "bottomleft", "bottomright"]:
            logging.warning(f"Position {position} not valid. Using topright instead.")
            self.__layer_control = ipyleaflet.LayersControl(position="topright")
            self.add(self.__layer_control)
        else:
            self.__layer_control = ipyleaflet.LayersControl(position=position)
            self.add(self.__layer_control)

    def remove_layer_control(self):
        """Remove the layer control from the map."""
        try:
            self.remove(self.__layer_control)
            del self.__layer_control
        except AttributeError:
            logging.warning(f"Layer control does not exist")

    def add_vector(self, name, url=None, geo_data=None, **kwargs):
        """Add a vector layer to the map.

        Params:
            name (str): The name of the vector layer
            url (str, path object or file-like object): Either the absolute or relative path to the file or URL to be opened, or any object with a read() method (such as an open file or StringIO)
            geo_data (geopandas.GeoDataFrame): A GeoDataFrame containing the vector data
            style (dict): A dictionary of Leaflet Path options
            hover_style (dict): A dictionary of Leaflet Path options
            point_style (dict): A dictionary of Leaflet Path options

        Returns:
            None

        Examples:
            ```python
            m = LeafMap.Map()
            m.add_vector(name='countries', url='https://ipyleaflet.readthedocs.io/en/latest/_downloads/countries.geo.json', style={'color': 'black', 'fillColor': '#3366cc', 'opacity':0.05, 'weight':1.9, 'dashArray':'2', 'fillOpacity':0.6}, hover_style={'fillColor': 'red' }, point_style={'radius': 5, 'color': 'red', 'fillOpacity': 0.8, 'fillColor': 'blue', 'weight': 3, 'type':'circle'})
            ```
        """

        if url is None and geo_data is None:
            logging.warning(f"Please provide either a URL or a GeoDataFrame.")
            return
        if url is not None and geo_data is not None:
            logging.warning(f"Please provide only one of URL or GeoDataFrame.")
            return

        if url is not None:
            try:
                gdf = gpd.read_file(url)
                geo_data = ipyleaflet.GeoData(geo_dataframe=gdf, name=name, **kwargs)
                self.__layers[name] = geo_data
                self.add(geo_data)
                return
            except Exception as e:
                logging.warning(f"There was an error adding the vector layer: {e}")
        if geo_data is not None:
            try:
                geo_data = ipyleaflet.GeoData(
                    geo_dataframe=geo_data, name=name, **kwargs
                )
                self.__layers[name] = geo_data
                self.add(geo_data)
                return
            except Exception as e:
                logging.warning(f"There was an error adding the vector layer: {e}")

    def add_raster(self, url, name, colormap=None, opacity=1.0, **kwargs):
        """Add a raster layer to the map.

        Params:
            url (str): The URL of the raster layer
            name (str): The name of the raster layer
            colormap (str): The colormap to use for the raster layer
            opacity (float): The opacity of the raster layer
            **kwargs: Additional keyword arguments

        Returns:
            None

        Examples:
            ```python
            m = LeafMap.Map()
            m.add_raster(url='https://example.com/raster.tif', name='raster', colormap='viridis', opacity=0.5)
            ```
        """
        from localtileserver import TileClient, get_leaflet_tile_layer

        if url is None:
            logging.warning(f"Please provide a URL.")
            return

        try:
            client = TileClient(url)
            raster_layer = get_leaflet_tile_layer(
                client, name=name, colormap=colormap, opacity=opacity, **kwargs
            )
            self.__layers[name] = raster_layer
            self.add(raster_layer)
            self.center = client.center()
            self.zoom = client.default_zoom
        except Exception as e:
            logging.warning(f"There was an error adding the raster layer: {e}")

    def add_image(self, url, bounds=None, opacity=1.0, **kwargs):
        """Add an image layer to the map.

        Params:
            url (str): The URL of the image layer
            bounds (tuple): The bounds of the image layer ((south, west), (north, east))
            opacity (float): The opacity of the image layer
            **kwargs: Additional keyword arguments

        Returns:
            None

        Examples:
            ```python
            m = LeafMap.Map()
            m.add_image(url='https://example.com/image.png', bounds=((40, -100), (30, -90)), opacity=0.5)
            ```
        """
        if url is None:
            logging.warning(f"Please provide a URL.")
            return

        if bounds is None:
            bounds = ((-90, -180), (90, 180))

        try:
            image_layer = ipyleaflet.ImageOverlay(
                url=url, bounds=bounds, opacity=opacity, **kwargs
            )
            self.add(image_layer)
            self.fit_bounds(bounds)
        except Exception as e:
            logging.warning(f"There was an error adding the image layer: {e}")

    def add_video(self, url, bounds=None, opacity=1.0, **kwargs):
        """Add a video layer to the map.

        Params:
            url (str): The URL of the video layer
            bounds (tuple): The bounds of the video layer ((south, west), (north, east))
            opacity (float): The opacity of the video layer
            **kwargs: Additional keyword arguments

        Returns:
            None

        Examples:
            ```python
            m = LeafMap.Map()
            m.add_video(url='https://example.com/video.mp4', bounds=((40, -100), (30, -90)), opacity=0.5)
            ```
        """
        if url is None:
            logging.warning(f"Please provide a URL.")
            return
        if bounds is None:
            bounds = ((13, -130), (32, -100))

        try:
            video_layer = ipyleaflet.VideoOverlay(
                url=url, opacity=opacity, bounds=bounds, **kwargs
            )
            self.add(video_layer)
            self.fit_bounds(bounds)
        except Exception as e:
            logging.warning(f"There was an error adding the video layer: {e}")

    def add_wms_layer(
        self, url, layers, name, format="image/png", transparent=True, **kwargs
    ):
        """Add a WMS layer to the map.

        Params:
            url (str): The URL of the WMS layer
            layers (str): The layers of the WMS layer
            name (str): The name of the WMS layer
            format (str): The format of the WMS layer
            transparent (bool): Whether the WMS layer is transparent
            **kwargs: Additional keyword arguments

        Returns:
            None

        Examples:
            ```python
            m = LeafMap.Map()
            m.add_wms_layer(url="https://ows.terrestris.de/osm/service",
                layers="OSM-WMS",
                name="WMS Layer",
                format="image/png",
                transparent=True,
            )
            ```
        """
        if url is None:
            logging.warning(f"Please provide a URL.")
            return

        try:
            wms_layer = ipyleaflet.WMSLayer(
                url=url,
                layers=layers,
                name=name,
                format=format,
                transparent=transparent,
                **kwargs,
            )
            self.__layers[name] = wms_layer
            self.add(wms_layer)
        except Exception as e:
            logging.warning(f"There was an error adding the WMS layer: {e}")

    def add_basemap_gui(self, position="topright"):
        """Add a basemap GUI to the map.

        This method creates a dropdown menu to select the basemap.
        The selected basemap is then applied to the map.

        Params:
            position (str): The position of the control (one of the map corners), can be 'topleft', 'topright', 'bottomleft' or 'bottomright'

        Returns:
            None

        """
        from ipywidgets import Dropdown, HBox, Button, Layout
        from ipyleaflet import basemaps, WidgetControl

        basemap_options = {
            "OpenStreetMap.Mapnik": basemaps.OpenStreetMap.Mapnik,
            "OpenTopoMap": basemaps.OpenTopoMap,
            "Esri.WorldImagery": basemaps.Esri.WorldImagery,
            "CartoDB.Positron": basemaps.CartoDB.Positron,
        }

        dropdown = Dropdown(
            options=basemap_options,
            description="Basemap:",
            value=basemaps.OpenStreetMap.Mapnik,
            layout=Layout(display="block", width="auto"),
        )
        button = Button(
            icon="times",
            button_style="primary",
            layout=Layout(width="35px", height="35px"),
        )

        def toggle_dropdown(b):
            if dropdown.layout.display == "none":
                dropdown.layout.display = "block"
                button.icon = "times"
            else:
                dropdown.layout.display = "none"
                button.icon = "chevron-left"

        def handle_dropdown_change(change):
            from ipyleaflet import basemap_to_tiles

            if change["new"] != change["old"]:
                self.substitute_layer(self.layers[0], basemap_to_tiles(change["new"]))
                dropdown.value = change["new"]

        dropdown.observe(handle_dropdown_change, names="value")

        button.on_click(toggle_dropdown)
        self.add_control(
            WidgetControl(widget=HBox([dropdown, button]), position=position)
        )
