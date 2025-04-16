import numpy as np
import numpy.ma as ma
import matplotlib
import pygimli as pg
from pygimli.viewer.mpl.colorbar import cmapFromName
matplotlib.use('Qt5Agg')
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
from matplotlib import pyplot as plt
import matplotlib.cm as cm
from mpl_toolkits.axes_grid1 import make_axes_locatable
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QTabWidget, QSplitter, QLabel
from PyQt5.QtCore import Qt

class InversionVisualizer(QMainWindow):
    def __init__(self, refrac_manager, inversion_params=None, parent=None):
        super().__init__(parent)
        self.refrac_manager = refrac_manager
        
        # Store inversion parameters or use defaults
        self.pg_vTop = 300 
        self.pg_vBottom = 3000
        self.pg_lam = 30
        self.pg_zWeight = 0.5
        
        # Override with provided parameters if available
        if inversion_params:
            if 'vTop' in inversion_params:
                self.pg_vTop = inversion_params['vTop']
            if 'vBottom' in inversion_params:
                self.pg_vBottom = inversion_params['vBottom']
            if 'lam' in inversion_params:
                self.pg_lam = inversion_params['lam']
            if 'zWeight' in inversion_params:
                self.pg_zWeight = inversion_params['zWeight']
                
        self.initUI()
        
    def initUI(self):
        self.setWindowTitle("Inversion Results Visualization")
        screen = QApplication.primaryScreen()
        screen_size = screen.size()
        self.resize(int(screen_size.width() * 0.9), int(screen_size.height() * 0.9))  # Resize to 90% of the screen size
        
        # Main widget and layout
        mainWidget = QWidget()
        self.setCentralWidget(mainWidget)
        mainLayout = QVBoxLayout(mainWidget)
        
        # Create tab widget for multiple views
        tabWidget = QTabWidget()
        mainLayout.addWidget(tabWidget)
        
        # Tab 1: Models
        modelsTab = QWidget()
        modelsLayout = QVBoxLayout(modelsTab)
        
        # Create a main splitter for horizontal division
        modelsMainSplitter = QSplitter(Qt.Horizontal)
        modelsLayout.addWidget(modelsMainSplitter)
        
        # Left splitter for top-left and bottom-left subplots
        modelsLeftSplitter = QSplitter(Qt.Vertical)
        modelsMainSplitter.addWidget(modelsLeftSplitter)
        
        # Right splitter for top-right and bottom-right subplots
        modelsRightSplitter = QSplitter(Qt.Vertical)
        modelsMainSplitter.addWidget(modelsRightSplitter)
        
        # Top-left: Starting Model
        startingModelWidget = QWidget()
        startingModelLayout = QVBoxLayout(startingModelWidget)
        startingModelTitle = QLabel("Starting model")
        startingModelTitle.setStyleSheet("font-weight: bold; font-size: 14px;")
        startingModelLayout.addWidget(startingModelTitle)
        startingFig = Figure(figsize=(5, 4), dpi=100)
        startingCanvas = FigureCanvas(startingFig)
        startingToolbar = NavigationToolbar(startingCanvas, self)
        startingModelLayout.addWidget(startingToolbar)
        startingModelLayout.addWidget(startingCanvas)
        startingAx = startingFig.add_subplot(111)
        self.plotStartingModel(startingAx)
        modelsLeftSplitter.addWidget(startingModelWidget)
        
        # Bottom-left: Inverted Model
        invertedModelWidget = QWidget()
        invertedModelLayout = QVBoxLayout(invertedModelWidget)
        invertedModelTitle = QLabel("Inverted model")
        invertedModelTitle.setStyleSheet("font-weight: bold; font-size: 14px;")
        invertedModelLayout.addWidget(invertedModelTitle)
        invertedFig = Figure(figsize=(5, 4), dpi=100)
        invertedCanvas = FigureCanvas(invertedFig)
        invertedToolbar = NavigationToolbar(invertedCanvas, self)
        invertedModelLayout.addWidget(invertedToolbar)
        invertedModelLayout.addWidget(invertedCanvas)
        invertedAx = invertedFig.add_subplot(111)
        self.plotInvertedModel(invertedAx)
        modelsLeftSplitter.addWidget(invertedModelWidget)
        
        # Top-right: Model with Rays
        raysModelWidget = QWidget()
        raysModelLayout = QVBoxLayout(raysModelWidget)
        raysModelTitle = QLabel("Inverted model with ray paths")
        raysModelTitle.setStyleSheet("font-weight: bold; font-size: 14px;")
        raysModelLayout.addWidget(raysModelTitle)
        raysFig = Figure(figsize=(5, 4), dpi=100)
        raysCanvas = FigureCanvas(raysFig)
        raysToolbar = NavigationToolbar(raysCanvas, self)
        raysModelLayout.addWidget(raysToolbar)
        raysModelLayout.addWidget(raysCanvas)
        raysAx = raysFig.add_subplot(111)
        self.plotModelWithRays(raysAx)
        modelsRightSplitter.addWidget(raysModelWidget)
        
        # Bottom-right: Coverage Masked Model
        coverageWidget = QWidget()
        coverageLayout = QVBoxLayout(coverageWidget)
        coverageTitle = QLabel("Inverted model with coverage mask")
        coverageTitle.setStyleSheet("font-weight: bold; font-size: 14px;")
        coverageLayout.addWidget(coverageTitle)
        coverageFig = Figure(figsize=(5, 4), dpi=100)
        coverageCanvas = FigureCanvas(coverageFig)
        coverageToolbar = NavigationToolbar(coverageCanvas, self)
        coverageLayout.addWidget(coverageToolbar)
        coverageLayout.addWidget(coverageCanvas)
        coverageAx = coverageFig.add_subplot(111)
        self.plotMaskedModel(coverageAx)
        modelsRightSplitter.addWidget(coverageWidget)
        
        # Add the models tab to the tab widget
        tabWidget.addTab(modelsTab, "Models")
        
        # Tab 2: Traveltimes
        traveltimesTab = QWidget()
        traveltimesLayout = QHBoxLayout(traveltimesTab)
        
        # Create a splitter for adjustable panels
        ttMainSplitter = QSplitter(Qt.Horizontal)
        traveltimesLayout.addWidget(ttMainSplitter)

        # Create a splitter for adjustable panels (left side)
        ttLeftSplitter = QSplitter(Qt.Vertical)
        ttMainSplitter.addWidget(ttLeftSplitter)        

        # Create a splitter for adjustable panels (right side)
        ttRightSplitter = QSplitter(Qt.Vertical)
        ttMainSplitter.addWidget(ttRightSplitter)
        
        # Traveltime curves figure
        ttCurvesWidget = QWidget()
        ttCurvesLayout = QVBoxLayout(ttCurvesWidget)
        ttCurvesTitle = QLabel("Traveltime curves")
        ttCurvesTitle.setStyleSheet("font-weight: bold; font-size: 14px;")
        ttCurvesLayout.addWidget(ttCurvesTitle)
        ttCurvesFig = Figure(figsize=(5, 4), dpi=100)
        ttCurvesCanvas = FigureCanvas(ttCurvesFig)
        ttCurvesToolbar = NavigationToolbar(ttCurvesCanvas, self)
        ttCurvesLayout.addWidget(ttCurvesToolbar)
        ttCurvesLayout.addWidget(ttCurvesCanvas)
        ttCurvesAx = ttCurvesFig.add_subplot(111)
        self.plotTraveltimeCurves(ttCurvesAx)
        ttLeftSplitter.addWidget(ttCurvesWidget)

        # Rays with travel time difference figure
        ttRaysWidget = QWidget()
        ttRaysLayout = QVBoxLayout(ttRaysWidget)
        ttRaysTitle = QLabel("Rays with traveltime difference")
        ttRaysTitle.setStyleSheet("font-weight: bold; font-size: 14px;")
        ttRaysLayout.addWidget(ttRaysTitle)
        ttRaysFig = Figure(figsize=(5, 4), dpi=100)
        ttRaysCanvas = FigureCanvas(ttRaysFig)
        ttRaysToolbar = NavigationToolbar(ttRaysCanvas, self)
        ttRaysLayout.addWidget(ttRaysToolbar)
        ttRaysLayout.addWidget(ttRaysCanvas)
        ttRaysAx = ttRaysFig.add_subplot(111)
        self.plotRaysWithTravelTimeDiff(ttRaysAx, time_in_ms=True, cmap='bwr')
        ttLeftSplitter.addWidget(ttRaysWidget)
        
        # observed vs simulated figure
        ttComparisonWidget = QWidget()
        ttComparisonLayout = QVBoxLayout(ttComparisonWidget)
        ttComparisonTitle = QLabel("Observed vs simulated traveltimes")
        ttComparisonTitle.setStyleSheet("font-weight: bold; font-size: 14px;")
        ttComparisonLayout.addWidget(ttComparisonTitle)
        ttComparisonFig = Figure(figsize=(5, 4), dpi=100)
        ttComparisonCanvas = FigureCanvas(ttComparisonFig)
        ttComparisonToolbar = NavigationToolbar(ttComparisonCanvas, self)
        ttComparisonLayout.addWidget(ttComparisonToolbar)
        ttComparisonLayout.addWidget(ttComparisonCanvas)
        ttComparisonAx = ttComparisonFig.add_subplot(111)
        self.plotTraveltimeComparison(ttComparisonAx)
        ttRightSplitter.addWidget(ttComparisonWidget)

        # Histogram of traveltimes difference
        histogramWidget = QWidget()
        histogramLayout = QVBoxLayout(histogramWidget)
        histogramTitle = QLabel("Histogram of traveltime relative differences")
        histogramTitle.setStyleSheet("font-weight: bold; font-size: 14px;")
        histogramLayout.addWidget(histogramTitle)
        histogramFig = Figure(figsize=(5, 4), dpi=100)
        histogramCanvas = FigureCanvas(histogramFig)
        histogramToolbar = NavigationToolbar(histogramCanvas, self)
        histogramLayout.addWidget(histogramToolbar)
        histogramLayout.addWidget(histogramCanvas)
        histogramAx = histogramFig.add_subplot(111)
        self.plotHistogram(histogramAx, data_type='rel_diff', bins=30, time_in_ms=True)
        ttRightSplitter.addWidget(histogramWidget)
        
        tabWidget.addTab(traveltimesTab, "Traveltimes")

        # Tab 3: Acquisition Setup
        setupTab = QWidget()
        setupLayout = QVBoxLayout(setupTab)

        # Create a main splitter for horizontal division
        setupMainSplitter = QSplitter(Qt.Horizontal)
        setupLayout.addWidget(setupMainSplitter)

        # Left splitter for top-left and bottom-left subplots
        setupLeftSplitter = QSplitter(Qt.Vertical)
        setupMainSplitter.addWidget(setupLeftSplitter)

        # Right splitter for top-right and bottom-right subplots
        setupRightSplitter = QSplitter(Qt.Vertical)
        setupMainSplitter.addWidget(setupRightSplitter)

        # Top-left: Setup with observed traveltimes
        observedWidget = QWidget()
        observedLayout = QVBoxLayout(observedWidget)
        observedTitle = QLabel("Observed traveltimes")
        observedTitle.setStyleSheet("font-weight: bold; font-size: 14px;")
        observedLayout.addWidget(observedTitle)
        observedFig = Figure(figsize=(5, 4), dpi=100)
        observedCanvas = FigureCanvas(observedFig)
        observedToolbar = NavigationToolbar(observedCanvas, self)
        observedLayout.addWidget(observedToolbar)
        observedLayout.addWidget(observedCanvas)
        observedAx = observedFig.add_subplot(111)
        self.plotSetup(observedAx, color_by='observed', time_in_ms=True, colormap='plasma')
        setupLeftSplitter.addWidget(observedWidget)

        # Bottom-left: Setup with simulated traveltimes
        simulatedWidget = QWidget()
        simulatedLayout = QVBoxLayout(simulatedWidget)
        simulatedTitle = QLabel("Simulated traveltimes")
        simulatedTitle.setStyleSheet("font-weight: bold; font-size: 14px;")
        simulatedLayout.addWidget(simulatedTitle)
        simulatedFig = Figure(figsize=(5, 4), dpi=100)
        simulatedCanvas = FigureCanvas(simulatedFig)
        simulatedToolbar = NavigationToolbar(simulatedCanvas, self)
        simulatedLayout.addWidget(simulatedToolbar)
        simulatedLayout.addWidget(simulatedCanvas)
        simulatedAx = simulatedFig.add_subplot(111)
        self.plotSetup(simulatedAx, color_by='simulated', time_in_ms=True, colormap='plasma')
        setupLeftSplitter.addWidget(simulatedWidget)

        # Top-right: Setup with difference
        DiffWidget = QWidget()
        DiffLayout = QVBoxLayout(DiffWidget)
        DiffTitle = QLabel("Traveltime differences")
        DiffTitle.setStyleSheet("font-weight: bold; font-size: 14px;")
        DiffLayout.addWidget(DiffTitle)
        DiffFig = Figure(figsize=(5, 4), dpi=100)
        DiffCanvas = FigureCanvas(DiffFig)
        DiffToolbar = NavigationToolbar(DiffCanvas, self)
        DiffLayout.addWidget(DiffToolbar)
        DiffLayout.addWidget(DiffCanvas)
        DiffAx = DiffFig.add_subplot(111)
        self.plotSetup(DiffAx, color_by='diff', time_in_ms=True, colormap='bwr')
        setupRightSplitter.addWidget(DiffWidget)

        # Bottom-right: Setup with relative difference
        relDiffWidget = QWidget()
        relDiffLayout = QVBoxLayout(relDiffWidget)
        relDiffTitle = QLabel("Relative traveltime differences")
        relDiffTitle.setStyleSheet("font-weight: bold; font-size: 14px;")
        relDiffLayout.addWidget(relDiffTitle)
        relDiffFig = Figure(figsize=(5, 4), dpi=100)
        relDiffCanvas = FigureCanvas(relDiffFig)
        relDiffToolbar = NavigationToolbar(relDiffCanvas, self)
        relDiffLayout.addWidget(relDiffToolbar)
        relDiffLayout.addWidget(relDiffCanvas)
        relDiffAx = relDiffFig.add_subplot(111)
        self.plotSetup(relDiffAx, color_by='rel_diff', time_in_ms=True, colormap='bwr')
        setupRightSplitter.addWidget(relDiffWidget)

        # Add the setup tab to the tab widget
        tabWidget.addTab(setupTab, "Sources vs Receiver diagrams")                   

    def show_mesh_with_qt(self, ax, mesh, data=None, 
                         colorbar=True,
                         cMin=None, cMax=None, 
                         logScale=False, colormap='Spectral_r',
                         title=None, colorbar_label='Velocity (m/s)', 
                         draw_mesh_boundaries=True, draw_mesh=False,
                         **kwargs):
        
        try:
            # Adjust the subplot
            ax.figure.subplots_adjust(right=0.8)
            
            # Draw the model
            if data is not None:
                pc = pg.viewer.mpl.drawModel(ax=ax, 
                                        mesh=mesh,
                                        data=data,
                                        cMin=cMin, 
                                        cMax=cMax,
                                        logScale=logScale,
                                        colorBar=False,
                                        **kwargs)
            else:
                pc = pg.viewer.mpl.drawMesh(ax=ax,
                                            mesh=mesh)
            
            # Apply colormap
            if colormap:
                pc.set_cmap(cm.get_cmap(colormap))
            
            # Add edges of the mesh if requested
            if draw_mesh_boundaries:
                b = mesh.boundaries(mesh.boundaryMarkers() != 0)
                pg.viewer.mpl.drawSelectedMeshBoundaries(ax, b,
                                                    color=(0.0, 0.0, 0.0, 1.0),
                                                    linewidth=1.4)
                
            # Draw the full mesh if requested
            if draw_mesh:
                b = mesh.boundaries(mesh.boundaryMarkers() == 0)
                pg.viewer.mpl.drawSelectedMeshBoundaries(ax, b,
                                                color=(0.0, 0.0, 0.0, 1.0),
                                                linewidth=0.5)
            if colorbar:
                # Create divider for existing axes instance
                divider = make_axes_locatable(ax)
                
                # Add an axes to the right of the main axes
                cax = divider.append_axes("right", size="5%", pad=0.1)
                
                # Create colorbar in this new axes
                cbar = ax.figure.colorbar(pc, cax=cax)
                
                # Set the colorbar label
                cbar.set_label(colorbar_label, rotation=270, labelpad=20)
            
            # Add axis labels
            ax.set_xlabel('Distance (m)')
            ax.set_ylabel('Elevation (m)')

            # Set scale and aspect ratio
            ax.autoscale(enable=True, axis='both', tight=True)
            ax.set_aspect('equal')
            
            # Add title if provided
            if title:
                ax.set_title(title)
                
            return pc
        
        except Exception as e:
            print(f"Error plotting model: {e}")
            ax.text(0.5, 0.5, f"Error plotting model: {str(e)}", 
                    ha='center', va='center', transform=ax.transAxes)
            return None
    
    def plotStartingModel(self, ax):
        # Plot the starting model

        self.show_mesh_with_qt(ax=ax, 
                            mesh=self.refrac_manager.mesh,
                            data=1/self.refrac_manager.fop.startModel(), 
                            cMin=self.pg_vTop, cMax=self.pg_vBottom,
                            logScale=False, colormap='Spectral_r',
                            # title='Starting model', 
                            colorbar_label='Velocity (m/s)', 
                            draw_mesh_boundaries=True,
                            )
    
    def plotInvertedModel(self, ax):
        # Plot the inverted model

        self.show_mesh_with_qt(ax=ax, 
                            mesh=self.refrac_manager.mesh,
                            data=self.refrac_manager.model, 
                            cMin=self.pg_vTop, cMax=self.pg_vBottom,
                            logScale=False, colormap='Spectral_r',
                            # title='Inverted model', 
                            colorbar_label='Velocity (m/s)', 
                            draw_mesh_boundaries=True,
                            )
    
    def plotModelWithRays(self, ax):
        # Plot model with ray paths

        self.show_mesh_with_qt(ax=ax, 
                            mesh=self.refrac_manager.mesh,
                            data=self.refrac_manager.model, 
                            cMin=self.pg_vTop, cMax=self.pg_vBottom,
                            logScale=False, colormap='Spectral_r',
                            # title='Inverted model with ray paths', 
                            colorbar_label='Velocity (m/s)', 
                            draw_mesh_boundaries=True,
                            )
        # Add ray paths
        self.refrac_manager.drawRayPaths(ax=ax, color="1", alpha=0.25)
    
    def plotMaskedModel(self, ax):
        # Plot masked model

        model_data = self.refrac_manager.model
        coverage = self.refrac_manager.standardizedCoverage()        
        masked_data = ma.masked_where(coverage <= 0, model_data)
        
        self.show_mesh_with_qt(ax=ax, 
                            mesh=self.refrac_manager.mesh,
                            data=masked_data, 
                            cMin=self.pg_vTop, cMax=self.pg_vBottom,
                            logScale=False, colormap='Spectral_r',
                            # title='Inverted model masked with ray paths', 
                            colorbar_label='Velocity (m/s)', 
                            draw_mesh_boundaries=True,
                            )
    
    def plotRaysWithTravelTimeDiff(self, ax, color_by='rel_diff', 
                                time_in_ms=True, cmap='bwr', percentile=95,
                                min_width=0.5, max_width=3.0, add_title=False):
        # Plot ray paths with traveltime differences

        try:
            # Draw velocity model as background
            self.show_mesh_with_qt(ax=ax, 
                            mesh=self.refrac_manager.mesh,
                            data=None, 
                            colorbar=False,
                            colormap=None,
                            title=None, 
                            draw_mesh_boundaries=True)
            
            # Get data and response
            data = self.refrac_manager.data
            sim_data = self.refrac_manager.inv.response
            
            # Scale factor for time units
            scale_factor = 1000 if time_in_ms else 1
            
            # Get ray paths using the manager's method
            rayPaths = self.refrac_manager.getRayPaths()
            
            # Calculate traveltime differences
            shots = data.id("s")
            receivers = data.id("g")
            tt_diffs = []
            rr_rel_diffs = []
            
            for i, (s, g) in enumerate(zip(shots, receivers)):
                mask = (data['s'] == s) & (data['g'] == g)
                observed = data['t'][mask][0] * scale_factor
                simulated = sim_data[mask][0] * scale_factor
                tt_diffs.append(simulated - observed)
                rr_rel_diffs.append(100 * (simulated - observed) / observed)
            
            # Choose data and colormap based on color_by parameter
            if color_by == 'rel_diff':
                # Symmetric limits based on data
                vmax = np.percentile(np.abs(rr_rel_diffs), percentile)
                vmin = -vmax
                c_data = rr_rel_diffs
                # For line width calculation, use absolute values
                abs_data = np.abs(rr_rel_diffs)
                colorbar_label = 'Relative traveltime difference (%)' if time_in_ms else 'Relative traveltime difference (%)'
            elif color_by == 'diff':
                vmax = np.percentile(np.abs(tt_diffs), percentile)
                vmin = -vmax
                c_data = tt_diffs
                abs_data = np.abs(tt_diffs)
                colorbar_label = 'Traveltime difference (ms)' if time_in_ms else 'Traveltime difference (s)'
            elif color_by == 'observed':
                vmin = np.min(data['t'] * scale_factor)
                vmax = np.max(data['t'] * scale_factor)
                c_data = data['t'] * scale_factor
                abs_data = np.abs(data['t'] * scale_factor - np.mean(data['t'] * scale_factor))
                colorbar_label = 'Observed traveltime (ms)' if time_in_ms else 'Observed traveltime (s)'
            elif color_by == 'simulated':
                vmin = np.min(sim_data * scale_factor)
                vmax = np.max(sim_data * scale_factor)
                c_data = sim_data * scale_factor
                abs_data = np.abs(sim_data * scale_factor - np.mean(sim_data * scale_factor))
                colorbar_label = 'Simulated traveltime (ms)' if time_in_ms else 'Simulated traveltime (s)'

            # Calculate line widths with a non-linear scale for better visibility
            abs_diff_val = abs(np.array(c_data))
            if max(abs_data) > 0:
                # Use percentile for normalization to avoid outlier influence
                perc = np.percentile(abs_data, percentile)
                norm_abs_data = np.minimum(abs_diff_val / perc, np.ones_like(abs_diff_val))
            else:
                norm_abs_data = np.zeros_like(abs_data)
        
            # Invert and scale to min_width-max_width range
            # line_widths = max_width - (max_width - min_width) * norm_abs_data
            line_widths = min_width + (max_width - min_width) * norm_abs_data

            # Additional safety check to ensure width is within bounds
            line_widths = np.clip(line_widths, min_width, max_width)
            
            # Create colormap and normalizer for colors
            cmap_obj = plt.get_cmap(cmap)
            norm = plt.Normalize(vmin=vmin, vmax=vmax)
            
            # Create pairs of (ray_path, difference) and sort by absolute difference
            ray_data = list(zip(rayPaths, c_data, line_widths))
            # Sort by absolute value of difference (descending, so lowest will be plotted last)
            ray_data.sort(key=lambda x: -abs(x[1]))
            
            # Plot rays individually from smallest to largest difference
            for ray, diff, width in ray_data:               
                color = cmap_obj(norm(diff))
                ax.plot([p[0] for p in ray], [p[1] for p in ray], 
                        color=color, linewidth=width, alpha=0.7)
            
            # Add colorbar
            divider = make_axes_locatable(ax)
            cax = divider.append_axes("right", size="5%", pad=0.1)
            sm = plt.cm.ScalarMappable(cmap=cmap_obj, norm=norm)
            sm._A = []  # Empty array needed for ScalarMappable
            cbar = ax.figure.colorbar(sm, cax=cax)
            cbar.set_label(colorbar_label, rotation=270, labelpad=20)
            
            # Add title and annotation about line thickness
            if color_by == 'rel_diff' or color_by == 'diff':
                title = f'Ray paths colored by {color_by} (thicker = better fit)'
            else:
                title = f'Ray paths colored by {color_by} (thickness based on deviation from mean)'
            
            if add_title:
                ax.set_title(title)
            
        except Exception as e:
            print(f"Error plotting rays with traveltime differences: {e}")
            import traceback
            traceback.print_exc()
            ax.text(0.5, 0.5, f"Error plotting rays: {str(e)}", 
                    ha='center', va='center', transform=ax.transAxes)

    def plotTraveltimeCurves(self, ax):
        # Plot observed and simulated traveltime curves
        try:
            # self.refrac_manager.showFit(ax=ax,firstPicks=True)

            self.plotTravelTime(ax, 
                          time_in_ms=True,
                          cm_to_use='qualitative',  # or 'sequential'
                          qual_cm='tab10',
                          seq_cm='plasma',
                          show_source=True,
                          invert_yaxis=True)
            
        except Exception as e:
            print(f"Error plotting traveltime curves: {e}")
            ax.text(0.5, 0.5, "Error plotting traveltime curves", 
                    ha='center', va='center', transform=ax.transAxes)
    
    def plotTraveltimeComparison(self, ax):
        # Plot observed vs simulated traveltimes
        try:
            self.plotObsCalcResiduals(ax)
            
        except Exception as e:
            print(f"Error plotting traveltime comparison: {e}")
            ax.text(0.5, 0.5, "Error plotting traveltime comparison", 
                    ha='center', va='center', transform=ax.transAxes)
            
    def plotObsCalcResiduals(self, ax, nCols=32, time_error=2.5, percentile=95, add_title=False):

        # Compare observed and calculated TT
        tpick = np.array(self.refrac_manager.inv.dataVals)*1000
        tcalc = np.array(self.refrac_manager.inv.response)*1000
        terr = np.array(self.refrac_manager.inv.errorVals)*1000
        tresid = 100*((tcalc-tpick)/tpick)

        data_percentile = np.percentile(np.abs(tresid),percentile)

        # Adjust the subplot
        ax.figure.subplots_adjust(right=0.8)

        scatter = ax.scatter(x=tpick, y=tcalc, c=tresid, s=14,
                    cmap=cmapFromName(cmapname='bwr', ncols=nCols),
                    vmin = -data_percentile, 
                    vmax = data_percentile,
                    edgecolors='black', linewidths=0.5,
                    zorder=10)

        ax.plot([0,np.max([tpick,tcalc])],[0,np.max([tpick,tcalc])],
                'k-',alpha=0.5,linewidth=1)
        ax.plot([time_error,np.max([tpick,tcalc])+time_error],[0,np.max([tpick,tcalc])],
                'k--',alpha=0.5,linewidth=1)
        ax.plot([0,np.max([tpick,tcalc])],[time_error,np.max([tpick,tcalc])+time_error],
                'k--',alpha=0.5,linewidth=1)
        
        ax.set_xlim([0,np.max([tpick,tcalc])])
        ax.set_ylim([0,np.max([tpick,tcalc])])
        ax.set_xlabel('Observed traveltime (ms)')
        ax.set_ylabel('Simulated traveltime (ms)')

        if add_title:
            ax.set_title('Observed vs Simulated Traveltimes')

        # Create divider for existing axes instance
        divider = make_axes_locatable(ax)
        
        # Add an axes to the right of the main axes
        cax = divider.append_axes("right", size="5%", pad=0.1)
        
        # Create colorbar in this new axes       
        cbar = ax.figure.colorbar(scatter, cax=cax)
        cbar.set_label('Relative traveltime difference (%)', rotation=270, labelpad=20)

        ax.set_aspect('equal')

        fittext = "{2} iterations\nvTop: {0} m/s\nvBottom: {1} m/s\n$\lambda$: {3}\naRMS: {4} ms\nrRMS: {5} %\n$\chi^2$: {6}".format(
            pg.pf(np.min(1/self.refrac_manager.fop.startModel())),
            pg.pf(np.max(1/self.refrac_manager.fop.startModel())),
            pg.pf(self.refrac_manager.inv.iter),
            pg.pf(self.refrac_manager.inv.inv.getLambda()),
            pg.pf(pg.utils.rms(self.refrac_manager.data['t']-self.refrac_manager.inv.response)*1000),
            pg.pf(pg.utils.rrms(self.refrac_manager.data['t'], 
                                self.refrac_manager.inv.response)*100),
            pg.pf(self.refrac_manager.fw.chi2History[-1])
        )

        ax.text(0.025, 0.975, fittext,
                transform=ax.transAxes,
                horizontalalignment='left',
                verticalalignment='top',
                fontsize=8)
        
    def plotHistogram(self, ax, data_type='observed', bins=30, time_in_ms=True, 
                 show_stats=True, color='skyblue', edge_color='black', add_title=False):
        """Plot histogram of observed, simulated, or difference traveltimes"""
        try:
            # Get data from the refraction manager
            data = self.refrac_manager.data
            sim_data = self.refrac_manager.inv.response
            
            # Scale factor for time units
            scale_factor = 1000 if time_in_ms else 1
            
            # Get the data based on data_type
            if data_type == 'observed':
                plot_data = data['t'] * scale_factor
                title = 'Observed traveltimes'
                x_label = 'Traveltime (ms)' if time_in_ms else 'Traveltime (s)'
            
            elif data_type == 'simulated':
                plot_data = sim_data * scale_factor
                title = 'Simulated traveltimes'
                x_label = 'Traveltime (ms)' if time_in_ms else 'Traveltime (s)'
            
            elif data_type == 'diff':
                plot_data = (sim_data - data['t']) * scale_factor
                title = 'Traveltime differences'
                x_label = 'Traveltime difference (ms)' if time_in_ms else 'Traveltime difference (s)'
            
            elif data_type == 'rel_diff':
                plot_data = 100 * (sim_data - data['t']) / data['t']  # Percentage
                title = 'Relative traveltime differences'
                x_label = 'Relative traveltime difference (%)'
            
            # Plot the histogram
            n, bins_edges, patches = ax.hist(plot_data, bins=bins, color=color, 
                                            edgecolor=edge_color, alpha=0.75)
            
            # Get statistics
            mean_val = np.mean(plot_data)
            median_val = np.median(plot_data)
            std_val = np.std(plot_data)
            min_val = np.min(plot_data)
            max_val = np.max(plot_data)
            
            if show_stats:
                # Draw vertical lines for mean and median
                ax.axvline(mean_val, color='purple', linestyle='-', linewidth=1.5, label=f'Mean: {mean_val:.2f}')
                ax.axvline(median_val, color='green', linestyle='--', linewidth=1.5, label=f'Median: {median_val:.2f}')
                # Draw vertical lines for min and max
                ax.axvline(min_val, color='blue', linestyle='-', linewidth=1.5, label=f'Min: {min_val:.2f}')
                ax.axvline(max_val, color='red', linestyle='-', linewidth=1.5, label=f'Max: {max_val:.2f}')
                # Draw vertical lines for std deviation
                ax.axvline(mean_val + std_val, color='orange', linestyle=':', linewidth=1.5, label=f'Std Dev: {std_val:.2f}')
                ax.axvline(mean_val - std_val, color='orange', linestyle=':', linewidth=1.5)
                # Draw vertical lines for 95th percentile
                perc_95 = np.percentile(plot_data, 95)
                ax.axvline(perc_95, color='cyan', linestyle='-.', linewidth=1.5, label=f'$95_{{th}}$ Percentile: {perc_95:.2f}')
                # Draw vertical lines for 5th percentile
                perc_5 = np.percentile(plot_data, 5)
                ax.axvline(perc_5, color='magenta', linestyle='-.', linewidth=1.5, label=f'$5_{{th}}$ Percentile: {perc_5:.2f}')

                # Add legend for statistics
                ax.legend(loc='upper left', fontsize=8)
            
            # Add labels and title
            ax.set_xlabel(x_label)
            ax.set_ylabel('Frequency')
            ax.grid(True, linestyle=':', alpha=0.7)

            if add_title:
                ax.set_title(title)
            
        except Exception as e:
            print(f"Error plotting histogram: {e}")
            import traceback
            traceback.print_exc()
            ax.text(0.5, 0.5, f"Error plotting histogram: {str(e)}", 
                    ha='center', va='center', transform=ax.transAxes)
     
    def plotTravelTime(self, ax, time_in_ms=True, cm_to_use='qualitative', 
                  qual_cm='tab10', seq_cm='plasma', show_source=True, 
                  invert_yaxis=True, show_grid=True, add_title=False):
        """Plot travel time picks from PyGIMLI refraction manager with colormap options"""
        try:
            # Get data from the refraction manager
            data = self.refrac_manager.data
            sensor_positions = data.sensors().array()
            sim_data = self.refrac_manager.inv.response
            
            # Get unique source indices
            unique_sources = np.unique(data['s'])
            
            # Set scale factor based on time units
            scale_factor = 1000 if time_in_ms else 1
            t_label = 'Time (ms)' if time_in_ms else 'Time (s)'
            
            # Adjust subplot layout
            ax.figure.subplots_adjust(right=0.8)
            
            # Initialize lists to collect data for limits and plotting
            all_times = []
            all_distances = []
            source_positions = []
            travel_times_by_source = []
            sim_travel_times_by_source = []
            offsets_by_source = []
            receivers_by_source = []
            
            # Organize data by source
            for i, s in enumerate(unique_sources):
                # Get source position
                source_pos = sensor_positions[s, 0]
                source_positions.append(source_pos)
                
                # Get receivers and times for this source
                mask = data['s'] == s
                receivers = data['g'][mask]
                times = data['t'][mask] * scale_factor
                sim_times = sim_data[mask] * scale_factor
                
                # Get receiver positions 
                receiver_pos = [sensor_positions[g, 0] for g in receivers]
                offsets = np.array(receiver_pos) - source_pos
                
                # Store for plotting
                travel_times_by_source.append(times)
                sim_travel_times_by_source.append(sim_times)
                offsets_by_source.append(offsets)
                receivers_by_source.append(np.array(receiver_pos))
                
                # Collect for limits
                all_times.extend(times)
                all_distances.extend(receiver_pos)
            
            # Setup colormap based on selected type
            if cm_to_use == 'qualitative':
                cmap_obj = plt.get_cmap(qual_cm)
                # Determine number of discrete colors
                if hasattr(cmap_obj, 'colors'):
                    n_disc = len(cmap_obj.colors)
                else:
                    n_disc = 10  # fallback for continuous maps
                discrete_colors = [cmap_obj(i) for i in np.linspace(0, 1, n_disc, endpoint=False)]
                colors = [discrete_colors[i % n_disc] for i in range(len(unique_sources))]
                
            elif cm_to_use == 'sequential':
                # Normalize source positions between 0 and 1
                norm = plt.Normalize(vmin=min(source_positions), vmax=max(source_positions))
                cmap = plt.get_cmap(seq_cm)
                colors = cmap(norm(source_positions))
            
            # Plot traveltime curves for each source
            for i, source_pos in enumerate(source_positions):
                receivers = receivers_by_source[i]
                times = travel_times_by_source[i]
                sim_times = sim_travel_times_by_source[i]
                
                # Plot the travel time curve
                ax.plot(receivers, times, '-+', 
                    linewidth=0.75, color=colors[i], markersize=4,
                    label=f"Source at {source_pos:.1f}m")
                
                # Plot the simulated travel time curve
                ax.plot(receivers, sim_times, '--', 
                    linewidth=1, color=colors[i])
                
                # Show source position on x-axis
                if show_source:
                    ax.scatter(source_pos, 0, color=colors[i], marker='*', s=100, 
                            clip_on=False, zorder=10)                 

            # Add colorbar based on colormap type
            if cm_to_use == 'qualitative':
                # Create a discrete colormap and norm
                boundaries = np.arange(0, n_disc + 1)
                cmap_discrete = matplotlib.colors.ListedColormap(discrete_colors)
                norm_discrete = matplotlib.colors.BoundaryNorm(boundaries, cmap_discrete.N)
                
                # Create ScalarMappable for colorbar
                sm = plt.cm.ScalarMappable(cmap=cmap_discrete, norm=norm_discrete)
                sm._A = []  # dummy array for ScalarMappable
                
                # Create divider for proper colorbar placement
                divider = make_axes_locatable(ax)
                cax = divider.append_axes("right", size="5%", pad=0.1)
                
                # Create colorbar with ticks centered in each bin
                tick_locs = np.arange(0.5, n_disc, 1)
                cbar = ax.figure.colorbar(sm, cax=cax, ticks=tick_locs)
                cbar.set_ticklabels(np.arange(1, n_disc+1))
                cbar.set_label('Source Number (mod %d)' % n_disc, rotation=270, labelpad=20)
                
            elif cm_to_use == 'sequential':
                # Create a colorbar for sequential map
                sm = plt.cm.ScalarMappable(cmap=plt.get_cmap(seq_cm), 
                                        norm=plt.Normalize(vmin=min(source_positions), 
                                                        vmax=max(source_positions)))
                sm._A = []
                
                # Create divider for proper colorbar placement
                divider = make_axes_locatable(ax)
                cax = divider.append_axes("right", size="5%", pad=0.1)
                
                # Add colorbar
                cbar = ax.figure.colorbar(sm, cax=cax)
                cbar.set_label('Source Position (m)', rotation=270, labelpad=20)
            
            # Set labels and grid
            ax.set_xlabel('Distance (m)')
            ax.set_ylabel(t_label)
            
            if show_grid:
                ax.grid(True)
            
            if len(all_times) > 0:
                # Set reasonable limits
                time_margin = 0.1 * (max(all_times) - min(all_times))
                dist_margin = 0.1 * (max(all_distances) - min(all_distances))
                
                ax.set_xlim(min(all_distances) - dist_margin, max(all_distances) + dist_margin)
                ax.set_ylim(min(all_times) - time_margin, max(all_times) + time_margin)
                
                # Invert y-axis for geophysical convention
                if invert_yaxis:
                    ax.invert_yaxis()
            
            # Add title
            if add_title:
                ax.set_title('Traveltime Curves')
            
        except Exception as e:
            print(f"Error plotting traveltime curves: {str(e)}")
            ax.text(0.5, 0.5, f"Error plotting traveltime curves: {str(e)}", 
                    ha='center', va='center', transform=ax.transAxes)
            
    def plotSetup(self, ax, color_by='observed', time_in_ms=True, 
                  colormap='plasma', add_title=False):
        """Plot source-receiver grid with observed/simulated traveltimes"""
        try:
            # Get data from the refraction manager
            data = self.refrac_manager.data
            sensor_positions = data.sensors().array()
            
            # Get simulated data (response)
            sim_data = self.refrac_manager.inv.response
            
            # Scale factor for time units
            scale_factor = 1000 if time_in_ms else 1
            
            # Get unique source indices
            unique_sources = np.unique(data['s'])
            
            # Lists to collect all data points
            source_pos_list = []  # Source positions (y-axis)
            receiver_pos_list = []  # Receiver positions (x-axis)
            observed_times_list = []
            simulated_times_list = []
            
            # Get data for all source-receiver pairs
            for s in unique_sources:
                # Get source position
                source_pos = sensor_positions[s, 0]  # Using horizontal position only
                
                # Get receivers and times for this source
                mask = data['s'] == s
                receivers = data['g'][mask]
                observed_times = data['t'][mask] * scale_factor
                simulated_times = sim_data[mask] * scale_factor
                
                # Get receiver positions
                for r, obs_t, sim_t in zip(receivers, observed_times, simulated_times):
                    receiver_pos = sensor_positions[r, 0]  # Using horizontal position only
                    
                    # Store data
                    source_pos_list.append(source_pos)
                    receiver_pos_list.append(receiver_pos)
                    observed_times_list.append(obs_t)
                    simulated_times_list.append(sim_t)
            
            # Convert to arrays
            source_pos_array = np.array(source_pos_list)
            receiver_pos_array = np.array(receiver_pos_list)
            observed_times_array = np.array(observed_times_list)
            simulated_times_array = np.array(simulated_times_list)
            
            # Calculate differences
            diff = simulated_times_array - observed_times_array
            rel_diff = 100 * diff / observed_times_array  # as percentage

            cmap = plt.get_cmap(colormap)
            
            # Choose data and colormap based on color_by parameter
            if color_by == 'rel_diff':
                # Symmetric limits based on data
                vmax = np.percentile(np.abs(rel_diff), 95)  # 95th percentile for better visualization
                vmin = -vmax
                c_data = rel_diff
                colorbar_label = 'Relative traveltime difference (%)' if time_in_ms else 'Relative traveltime difference (%)'
            
            elif color_by == 'diff':
                vmax = np.percentile(np.abs(diff), 95)  # 95th percentile
                vmin = -vmax
                c_data = diff
                colorbar_label = 'Traveltime difference (ms)' if time_in_ms else 'Traveltime difference (s)'
            
            elif color_by == 'observed':               
                vmin = np.min(observed_times_array)
                vmax = np.max(observed_times_array)
                c_data = observed_times_array
                colorbar_label = 'Observed traveltime (ms)' if time_in_ms else 'Observed traveltime (s)'
            
            elif color_by == 'simulated':
                vmin = np.min(simulated_times_array)
                vmax = np.max(simulated_times_array)
                c_data = simulated_times_array
                colorbar_label = 'Simulated traveltime (ms)' if time_in_ms else 'Simulated traveltime (s)'
            
            # Plot scatter plot of receiver vs source
            sc = ax.scatter(receiver_pos_array, source_pos_array, 
                        s=10, c=c_data, cmap=cmap, vmin=vmin, vmax=vmax,
                        marker='s', edgecolors='black', linewidths=0.5)
            
            # Add colorbar
            divider = make_axes_locatable(ax)
            cax = divider.append_axes("right", size="5%", pad=0.1)
            cbar = ax.figure.colorbar(sc, cax=cax)
            cbar.set_label(colorbar_label, rotation=270, labelpad=20)
            
            # Set axis properties
            ax.set_xlabel('Receiver position (m)')
            ax.set_ylabel('Source position (m)')
            ax.grid(True, linestyle=':')
            ax.set_aspect('equal')
            
            # Set the title based on the coloring
            if color_by == 'observed': 
                title = 'Observed traveltime)'
            elif color_by == 'simulated':
                title = 'Simulated traveltime)'
            elif color_by == 'diff' or color_by == 'abs_diff':
                title = 'Traveltime difference)'
            elif color_by == 'rel_diff':
                title = 'Relative traveltime difference)'
            
            if add_title:
                ax.set_title(title)
            
        except Exception as e:
            print(f"Error plotting source-receiver grid: {e}")
            ax.text(0.5, 0.5, f"Error plotting source-receiver grid: {str(e)}", 
                    ha='center', va='center', transform=ax.transAxes)
        
def display_inversion_results(refrac_manager, inversion_params=None):
    """Helper function to display inversion results in a new window"""
    visualizer = InversionVisualizer(refrac_manager, inversion_params)
    visualizer.show()
    return visualizer  # Return it so it doesn't get garbage collected

