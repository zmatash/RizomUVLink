from win import rizomuvlink

CZEx = rizomuvlink.ZEx

class CRizomUVLinkBase:
	def __init__(self):
		#self.version = rizomuvlink.__version__
		self.rizomuv = rizomuvlink.RizomUVLinkPyd()
		self.name = "RizomUV Link"
		self.author = "remi.arquier at rizom-lab dot com"
		self.description = "An open source Python module to control a RizomUV instance from a DCC application."
		self.website = "https://rizom-lab.com"

	def Execute(self, command, parameters):
		return self.rizomuv.Execute(command, parameters)

	def BindUrl(self, url = "tcp://localhost:5555"):
		self.rizomuv.BindUrl(url)

	def LibTaskUpdate(self, p):
		"""
		Intended for internal use only
		"""
		return self.rizomuv.Execute('LibTaskUpdate', p)

	def PsExport(self, p):
		"""
		Export UV layout in a postscript file.
		"""
		return self.rizomuv.Execute('PsExport', p)

	def LibTaskEnd(self, p):
		"""
		Intended for internal use only
		"""
		return self.rizomuv.Execute('LibTaskEnd', p)

	def Load(self, p):
		"""
		Import mesh from a file or by provided vectors data
		
		Use either:
		
		  1. Data.* members to import mesh from provided vector data
		
		  2. File.* members to import mesh from fbx or OBJ files path from disk
		
		Remark: If you are using ##Data## and if you provide triangle data (polygon tessellation), the impor
		        ting task will not search for topology errors in the mesh. However the importing phase will 
		        be faster
		
		PARAMETER       : Data.PolySizes
		Brief           : Vertex count of each polygons [p0 p1 ... pn-1].
		Type            : ints
		
		PARAMETER       : Data.PolyXYZIDs
		Brief           : Polygons of the geometry in 3D Space
		Type            : ints
		
		Indexes toward 3D space coordinates list [p0v0 p0v1 p0v2 p0v3 p1v0 p1v1 p1v2 p1v3 ... pn-1v0 pn-1v1 
		pn-1v2 pn-1v3].
		
		
		PARAMETER       : Data.TriangleXYZID
		Brief           : 3D space triangles coming from the host application tessellation
		Type            : ints
		
		If there are specified, the importing method will not do the mesh topological tests. In that case th
		e mesh need to respect the following rules: 
		
		  1. No singular edges: All edges must be connected to 2 polygons maximum
		
		  2. No singular vertexes: All polygons connected to a given vertex must share an edge and form a si
		    ngle group (two cones cannot share the same apex vertex, even if the cones have some detached p
		    olygons)
		
		  3. Orientation consistency: There must be no discontinuity in the orientation of two given connect
		    ed triangles (no moebius strip).
		
		  4. No isolated vertexes: All vertexes of V must be connected to one triangle of T at least
		
		  5. No degenerated polygons: The vertex indices of all polygons must be different
		
		  6. Indexes toward 3D space coordinates list [t0v0 t0v1 t0v2 t1v0 t1v1 t1v2 t1v3 ... tn-1v0 tn-1v1 
		    tn-1v2]
		
		
		PARAMETER       : Data.CoordsXYZ
		Brief           : The 3D space coordinates of each vertex in raw format [x0 y0 z0 x1 y1 z1 ... xm-1 ym-1 zm-1]
		Type            : doubles
		
		PARAMETER       : Data.CoordsUVW
		Brief           : The UVW coordinates in raw format [u0 v0 w0 u1 v1 w1 u2 v2 w2 ... un-1 vn-1 wn-1]
		Type            : doubles
		
		PARAMETER       : Data.PolyUVWIDs
		Brief           : The UV space coordinates in raw format [u0 v0 w0 u1 v1 w1 u2 v2 w2 ... un-1 vn-1 wn-1]
		Type            : ints
		
		Remark:  The W coordinates must be included in that list even if its value is zero.
		
		
		PARAMETER       : Data.UnmappedPolyIDs
		Brief           : Polygon indexes that do not have any UV indices and UV coordinates.
		Type            : ints
		
		PARAMETER       : Data.Maps
		Brief           : Import a list of maps of type CDataMap.
		Type            : table (DataMap)
		
		PARAMETER       : Data.UseImportedUVWPolygons
		Brief           : Use imported UVW polygons topology .
		Type            : bool
		
		Use previously imported polygon UVW data. This will reorder the currently imported. UVW coordinates 
		list so that it will match the polygon UVW data imported in a previously made importing task.
		
		Remark:  This is intended to be used when ##Data.CoordsUVW## only is set. If ##Data.PolySizes## is s
		        pecified this flag is ignored. 
		
		Remark:  This is useful when the host application do not handle polygon UVW topology modification an
		        d when the mesh can have topology errors.
		
		
		PARAMETER       : Data.CoordsUVWPartial
		Brief           : Partial UVW coordinates set toward UVW coordinates
		Type            : table
		
		Remark: "Partial" means that the data do not necessary contains the uvs for all vertexes.
		
		 The pointed data must be a table formed like this:
		
		  1. a vector of integers (ints) named "PolyVertIDs" containing the PolyVertIDs of the vertexes
		
		  2. a vector of doubles (doubles) named "UVWs" containing the folded UVW coordinates [u0 v0 w0 u1 v
		    1 w1 u2 v2 w2 ... un-1 vn-1 wn-1]
		
		The vertex specified at position 2p in "PolyVertIDs" has the coordinates at position 3p, 3p+1, 3p+2 
		in the vector "UVWs"
		
		
		PARAMETER       : Data.CoordsUVWInternalPath
		Brief           : Internal path (into internal data tree) toward partial UVW coordinates
		Type            : string
		
		"Partial" means that the data do not necessary contains the uvs for all vertexes.
		
		 The pointed data must be a table formed like this:
		
		  1. a vector of integers (ints) named "PolyVertIDs" containing the PolyVertIDs of the vertexes
		
		  2. a vector of doubles (doubles) named "UVWs" containing the folded UVW coordinates [u0 v0 w0 u1 v
		    1 w1 u2 v2 w2 ... un-1 vn-1 wn-1]
		
		The vertex specified at position 2p in "PolyVertIDs" has the coordinates at position 3p, 3p+1, 3p+2 
		in the vector "UVWs"
		
		
		PARAMETER       : File.Path
		Brief           : Import mesh by loading an obj file on the file system so this is Path of the obj file.
		Type            : string
		
		PARAMETER       : File.FBX.UseUVSetNames
		Brief           : Use UV set's file names to order the UV Sets.
		Type            : bool
		
		When enabled, a UV set will be created for all UV set name found in the file. Objects that doesn't h
		ave any UV set in their UV set list, will be assigned a default UV set using the 3D coordinates of t
		he object.
		
		If disabled, UV channel index will be used to map the file's UV set to the API instance's UV sets. W
		hich mean that the final UV set count will be equal to the maximum of the UV set count found in all 
		objects of the scene. Object that has less UV sets than the maximum UV set count in the full scene w
		ill be assigned a default UV set using the 3D coordinates of the object.
		
		
		PARAMETER       : File.XYZ
		Brief           : Ignore all present UV space data present in the file and interpret 3D space data both as 3D and UVW input data.
		Type            : bool
		
		Remark: This option cannot be used simultaneously with ##File.XYZUVW##
		
		
		PARAMETER       : File.XYZUVW
		Brief           : Import both 3D and UVW data.
		Type            : bool
		
		Remark: This option cannot be used simultaneously with ##File.XYZ##
		
		
		PARAMETER       : File.UVWProps
		Brief           : Import UVW properties (constrained primitives)
		Type            : bool
		
		PARAMETER       : File.ImportGroups
		Brief           : Import polygon model groups like object, materials, smoothing and polygon groups
		Type            : bool
		
		PARAMETER       : DefaultUnit
		Brief           : Default unit of the file if the file doesn't provide it
		Type            : string
		
		This value is used by the packing algoriithm in case of texel density scaling mode is specified.
		
		Remark: OBJ files doesn't provide them so this value will be set. FBX file provides them sometimes.
		
		Remark: If the file doesn't provide the unit information, and if that paremeter is not specified, th
		        en the unit set using SetOption will be used.
		
		
		PARAMETER       : NormalizeUVW
		Brief           : Normalize the UVW coordinates into an unity cube
		Type            : bool
		
		PARAMETER       : File.UpAxis
		Brief           : Import specify the up axis
		Type            : string
		Default         : "y"
		
		Brief           : Import task return error codes
		Type            : 
		Possible Values :
		                 - IMPORT_TASK_SUCCES
		                 - IMPORT_TASK_FILE_NOT_FOUND
		                 - IMPORT_TASK_BAD_VERTEX_ID_POLY_V3D_LIST
		                 - IMPORT_TASK_BAD_VERTEX_ID_POLY_VT_LIST
		                 - IMPORT_TASK_BAD_VERTEX_ID_POLY_VN_LIST
		                 - IMPORT_TASK_MISFORMED_POLYGON_LISTS
		                 - IMPORT_TASK_TOPO_ERROR
		                 - IMPORT_TASK_WARNING_UVW_COUNT_LESS_THAN_3D_COUNT
		                 - IMPORT_TASK_FILE_CONTAINS_INCONSISTANT_DATA
		                 - IMPORT_TASK_FILE_IS_PASSWD_PROTECTED
		                 - IMPORT_TASK_FILE_HAS_NOT_THE_EXPECTED_FILE_FORMAT
		                 - IMPORT_TASK_FILE_FORMAT_VERSION_IS_NOT_HANDLED
		                 - IMPORT_TASK_FILE_OBJECT_CONTAINS_UNSUPORTER_CHARACTER
		                 - IMPORT_TASK_DATA_NOT_FOUND
		                 - IMPORT_TASK_FBX_SDK_NOT_PRESENT
		                 - IMPORT_TASK_UV_SET_HAS_EMPTY_NAME
		                 - IMPORT_TASK_OBJECTS_HAVE_INCONSISTANT_UV_SETS
		                 - IMPORT_TASK_WARNING_RIZOMUV_METADATA_FAILED_TO_LOAD
		
		
		"""
		return self.rizomuv.Execute('Load', p)

	def InitLib(self, p):
		"""
		Initialize the API
		
		PARAMETER       : UndoHistorySize
		Brief           : Size of the undo history
		Type            : int
		
		
		"""
		return self.rizomuv.Execute('InitLib', p)

	def RasterExport(self, p):
		"""
		Copy 3D coordinates to UVW space
		
		PARAMETER       : WorkingSet
		Brief           : The island set on which the task will be applied
		Type            : string
		Default         : "Visible"
		Possible Values :
		                 - Visible
		                 - Selected
		                 - Flat
		                 - NotFlat
		
		Remark: Combinations are possible like "Visible&Selected&Flat"
		
		
		PARAMETER       : FilePath
		Brief           : Exported file path
		Type            : string
		
		PARAMETER       : AASamples
		Brief           : Anti-alias sample count value
		Type            : int
		Default         : 1
		
		PARAMETER       : EdgePaddingSize
		Brief           : Edge padding size in pixel units
		Type            : double
		
		PARAMETER       : BackgroundColor
		Brief           : Polygon color mode if ##PolygonColorMode## == "Color"
		Type            : vector3d
		Default         : 1.0 1.0 1.0
		
		PARAMETER       : PolygonColor
		Brief           : Polygon color mode if ##PolygonColorMode## == "Color"
		Type            : vector3d
		Default         : 0.75 0.75 0.75
		
		PARAMETER       : PolygonColorMode
		Brief           : Rasterisation polygon fill mode mode
		Type            : string
		Default         : "Off"
		Possible Values :
		                 - "Off"        : Do not fill polygons
		                 - "Color"        : Fill mode using the specified color
		                 - "ColorIDMap"        : Render polygons using uniform colors contained into the island Properties.Color data field
		                 - "Stretches"        : Render polygons using triangle area ratio between UV space and 3D space
		
		PARAMETER       : EdgeColor
		Brief           : Edge color mode if ##EdgeColorMode## == "Color"
		Type            : vector3d
		Default         : 0.0 0.0 0.0
		
		PARAMETER       : EdgeColorMode
		Brief           : Specify on edges should be rendered
		Type            : string
		Default         : "Color"
		Possible Values :
		                 - "Off"        : Do not draw edges at all
		                 - "Color"        : Use the specified color
		
		PARAMETER       : BorderOnly
		Brief           : Draw border edges only
		Type            : bool
		
		PARAMETER       : Width
		Brief           : Width in specified unit
		Type            : double
		Default         : 512.0
		
		PARAMETER       : Height
		Brief           : Height in specified unit
		Type            : double
		Default         : 512.0
		
		PARAMETER       : WidthHeightUnit
		Brief           : Unity of width and height
		Type            : string
		Default         : "px"
		Possible Values :
		                 - "px"        : Pixel
		                 - "m"        : Meter
		                 - "cm"        : Centimeter
		                 - "mm"        : Millimeter
		                 - "in"        : Inch
		
		PARAMETER       : PrintResolution
		Brief           : Print resolution
		Type            : double
		Default         : 72.0
		
		PARAMETER       : PrintResolutionUnit
		Brief           : Print resolution unit
		Type            : string
		Default         : "px/cm"
		Possible Values :
		                 - "px/cm"
		                 - "px/mm"
		                 - "px/in"
		
		PARAMETER       : CroppingBox
		Brief           : Use a cropping box (the default is the UV unity square)
		Type            : box2d
		
		PARAMETER       : SelectedIslands
		Brief           : Draw selected islands only
		Type            : bool
		
		PARAMETER       : NoExportIfEmpty
		Brief           : Do not export if there is nothing to draw
		Type            : bool
		
		PARAMETER       : LZW
		Brief           : Use LZW compression for tiff files
		Type            : bool
		
		PARAMETER       : Stretches.Neutral
		Brief           : Stretch neutral value when ##PolygonColorMode## == "Stretches"
		Type            : double
		
		PARAMETER       : Stretches.Min
		Brief           : Stretch min value when ##PolygonColorMode## == "Stretches"
		Type            : double
		
		PARAMETER       : Stretches.Max
		Brief           : Stretch max value when ##PolygonColorMode## == "Stretches"
		Type            : double
		
		
		"""
		return self.rizomuv.Execute('RasterExport', p)

	def Save(self, p):
		"""
		Export mesh data into file or into data structures
		
		Use either:
		
		  1. Data.* members to export mesh vector data
		
		  2. File.* members to export mesh to fbx or OBJ files
		
		  3. IndexTable.* members to export island related data
		
		PARAMETER       : File
		Brief           : File mode table data
		Type            : table
		
		PARAMETER       : Data
		Brief           : Data mode table data
		Type            : table
		
		PARAMETER       : File.Path
		Brief           : Export all mesh data into obj file
		Type            : string
		
		The file extension will be used to recognise the file format
		
		
		PARAMETER       : File.UVWProps
		Brief           : Exports some UV properties such as constraints, symmetry, by island packing properties, tile(s) properties
		Type            : bool
		
		PARAMETER       : File.UVWInXYZ
		Brief           : Export the UVW space data in place of the 3D space
		Type            : table
		
		PARAMETER       : File.UVWInXYZ.CroppingBox
		Brief           : Export the UVW space into the 3D space and add a quad defined by the 2D box CroppingBox
		Type            : box2d
		
		PARAMETER       : IndexTable.VertexIDsToIslandIDs
		Brief           : Export indexing list that give the island ID from an vertex ID (vertex ID of UV Space topology)
		Type            : bool
		
		Remark: The mesh input must not contain any topology error
		
		
		PARAMETER       : IndexTable.PolygonIDsToIslandIDs
		Brief           : Export indexing list that give the island ID from a polygon ID
		Type            : bool
		
		PARAMETER       : File.FBX.Compatibilty
		Brief           : FBX export compatibility version string
		Type            : string
		
		Have a look at fbxio.h file of the FBX SDK for possible values
		
		Remark: Default export the last availabe version
		
		
		PARAMETER       : File.FBX.FormatDescriptor
		Brief           : The FBX file format descriptor
		Type            : string
		
		Use either:
		
		  - FBX binary (*.fbx)
		
		  - FBX ascii (*.fbx)
		
		  - FBX encrypted (*.fbx)
		
		  - FBX 6.0 binary (*.fbx)
		
		  - FBX 6.0 ascii (*.fbx)
		
		  - FBX 6.0 encrypted (*.fbx)
		
		  - AutoCAD DXF (*.dxf)
		
		  - Alias OBJ (*.obj)
		
		  - Collada DAE (*.dae)
		
		
		PARAMETER       : File.FBX.UseUVSetNames
		Brief           : Use UV Set names to select UV slots that already exist in the FBX file
		Type            : bool
		
		which means that the original sequence order present in the file will be kept, even if some fbx mesh
		es have their UV set in a different order.
		
		If the FBX file is organized like that:
		
		        				FBX MESH NAME | FBX LAYER | FBX UV SET NAME |
		        				-----------------------------------------
		        				Mesh 0              0         diffuse
		        									1         specular
		        				-----------------------------------------
		        				Mesh 1              0         specular
		        									1         diffuse
		        			  
		
		and if the UV Set names in RizomUV are like that:
		
		        				UV CHANNEL | UV SET NAME |
		        				--------------------------
		        				0         diffuse
		        				1         specular
		        			  
		
		then the file will keep the same order data organization.
		
		If disabled, the UV Set name present in the RizomUV will make authority and replace the one inside t
		he the FBX file:
		
		        				FBX MESH NAME | FBX LAYER | FBX UV SET NAME
		        				-----------------------------------------
		        				Mesh 0              0         diffuse
		        									1         specular
		        				-----------------------------------------
		        				Mesh 1              0         diffuse
		        									1         specular => has been reodered
		        			  
		
		
		PARAMETER       : File.FBX.PartialUVSets
		Brief           : Do not export UV polygons that have at least one UVW coordinates not in the UV plane.
		Type            : bool
		
		Which means that the UV nodes indexes will be equal to -1 in the fbx's index array of the UV element
		 object. Some software may not support this options. 
		
		
		PARAMETER       : File.FBX.DeleteUnusedUVSets
		Brief           : Do not export UV Set that have zero UV polygon situated in the UV plane.
		Type            : bool
		
		Remark: In presence of multiple UV sets, if such a completely unflattened UV set would be located in
		         the first UV Channel, the second UV channel (flattened) will be placed in the first one! 
		
		
		PARAMETER       : Data.UseImportedUVWPolygons
		Brief           : Export UVW coordinates using the imported UVW polygons
		Type            : bool
		
		This will export the UVW coordinates vector compatible to the imported polygon topology, so the numb
		er of UVW vertices will be the same has imported. This has no effect when the imported mesh is free 
		from topology errors and if there is not cut/welding operation but useful when the unfold library ha
		s repaired (added some vertices/changed the UVW polygons) and when host program cannot handle UVW sp
		ace topology changes.It means also that if the topology has changed since the import,there will be s
		ome strange lines (formed by edges) linking some UVW vertices.
		
		Remark: If that option is set, ONLY the coordinates ##Data.CoordsUVW## will be exported, and NOT the
		         polygonUVW data. However the selected vertices will be ALWAYS exported
		
		
		PARAMETER       : ReframeBox
		Brief           : Reframe the UV coordinates into a specified 2D Box
		Type            : box2d
		
		OUTPUT      : Data.PolySizes
		Brief           : Vertex count of each polygons [p0 p1 ... pn-1]
		Type            : ints
		
		OUTPUT      : Data.PolyUVWIDs
		Brief           : Indexes toward UVW space coordinates list [p0v0 p0v1 p0v2 p0v3 p1v0 p1v1 p1v2 p1v3 ... pn-1v0 pn-1v1 pn-1v2 pn-1v3]
		Type            : ints
		
		OUTPUT      : Data.CoordsUVW
		Brief           : The UVW coordinates in raw format [u0 v0 w0 u1 v1 w1 ... ut-1 vt-1 wt-1]
		Type            : doubles
		
		OUTPUT      : Data.SelectedVertIDs
		Brief           : The selected vertIDs selection (corresponding to the current internal mesh UVW polygons representation)
		Type            : ints
		
		OUTPUT      : IndexTable.VertexIDsToIslandIDs
		Brief           : Indexing list that give the island ID from an vertex ID (vertex ID of UV Space topology)
		Type            : ints
		
		OUTPUT      : IndexTable.PolygonIDsToIslandIDs
		Brief           : Export indexing list that give the island ID from a polygon ID
		Type            : ints
		
		Brief           : Export task return error codes
		Type            : 
		Possible Values :
		                 - EXPORT_TASK_SUCCES
		                 - EXPORT_TASK_MISFORMED_FILE_PATH
		                 - EXPORT_TASK_UNKNOWN_FILE_EXTENTION
		                 - EXPORT_TASK_FAILED_TO_OPEN_FILE_FOR_WRITING
		                 - EXPORT_TASK_IMPOSED_UVW_POLYGON_HAS_INCORRECT_SIZE
		                 - EXPORT_TASK_IMPOSED_UVW_POLYGON_LIST_HAS_INCORRECT_SIZE
		                 - EXPORT_TASK_IMPOSED_UVW_LIST_HAS_INCORRECT_SIZE
		                 - EXPORT_TASK_INVALID_FILE_VERSION
		                 - EXPORT_TASK_INSUFFICIENT_MEMORY
		                 - EXPORT_TASK_INVALID_PARAMETER
		                 - EXPORT_TASK_INVALID_FILE
		                 - EXPORT_TASK_INDEX_OUT_OF_RANGE
		                 - EXPORT_TASK_PASSWORD_ERROR
		                 - EXPORT_TASK_FBX_SDK_NOT_COMPILED
		
		PARAMETER       : File.FBX.DontRecycleUVElements
		Brief           : Deleted UVs in session will leave FBX layers as they are (probably without UV mapping elements)
		Type            : bool
		
		
		"""
		return self.rizomuv.Execute('Save', p)

	def PaintMap(self, p):
		"""
		Modify map values
		"""
		return self.rizomuv.Execute('PaintMap', p)

	def Hide(self, p):
		"""
		Hide and reveal elements
		
		PARAMETER       : PrimType
		Brief           : Processed primitive type
		Type            : string
		Default         : "Vertex"
		Possible Values :
		                 - "Vertex"
		                 - "Edge"
		                 - "Triangle"
		                 - "Island"
		
		PARAMETER       : Hide
		Brief           : Select hiding mode
		Type            : bool
		
		PARAMETER       : Isolate
		Brief           : Select isolate mode
		Type            : bool
		
		PARAMETER       : Show
		Brief           : Select show mode
		Type            : bool
		
		PARAMETER       : UseList
		Brief           : List of primitive indexes
		Type            : ints
		
		Remark: This list will be used as input
		
		
		PARAMETER       : UseSelection
		Brief           : Use selection set as input
		Type            : bool
		
		PARAMETER       : UseAll
		Brief           : Use all primitives as input
		Type            : bool
		
		PARAMETER       : Deselect
		Brief           : Deselect as post operation
		Type            : bool
		
		
		"""
		return self.rizomuv.Execute('Hide', p)

	def Cut(self, p):
		"""
		Separate UV polygons using edge set or polygon set limits
		
		Remark: Some UV vertexes are duplicated in UV space, so the UV topology is changed
		
		PARAMETER       : PrimType
		Brief           : The primitive type used to determine the processed set
		Type            : string
		Default         : "Edge"
		Possible Values :
		                 - "Edge"
		                 - "Triangle"
		
		Remark: "Polygon" primitive mode is not available for now
		
		
		PARAMETER       : WorkingSet
		Brief           : The island set on which the task will be applied
		Type            : string
		Default         : "Visible&UnLocked"
		Possible Values :
		                 - "Visible"
		                 - "Selected"
		                 - "Flat"
		                 - "NotFlat"
		
		Remark: Combinations are possible like "Visible&Selected&Flat"
		
		
		PARAMETER       : IDs
		Brief           : List of primitive indexes
		Type            : ints
		
		Use primitives indexes instead of the selection states
		
		
		
		"""
		return self.rizomuv.Execute('Cut', p)

	def Weld(self, p):
		"""
		Connect UV polygons
		
		Remark: Some UV vertexes are duplicated in UV space, so the UV topology is changed
		
		PARAMETER       : PrimType
		Brief           : The primitive type used to determine the processed set
		Type            : string
		Default         : "Edge"
		Possible Values :
		                 - "Edge"
		                 - "Triangle"
		                 - "Island"
		
		Remark: "Polygon" primitive mode is not available for now
		
		
		PARAMETER       : WorkingSet
		Brief           : The island set on which the task will be applied
		Type            : string
		Default         : "Visible&UnLocked"
		Possible Values :
		                 - "Visible"
		                 - "Selected"
		                 - "Flat"
		                 - "NotFlat"
		
		Remark: Combinations are possible like "Visible&Selected&Flat"
		
		
		PARAMETER       : IDs
		Brief           : List of primitive indexes
		Type            : ints
		
		Use primitives indexes instead of the selection states
		
		
		PARAMETER       : Mode
		Brief           : Welding Mode
		Type            : string
		Default         : "All"
		Possible Values :
		                 - "All"        : All selected or specified primitives (using ##IDs##) will be welded
		                 - "SelfIslands"        : All selected or specified primitives (using ##IDs##) that have their opposite part in the same island will be welded
		                 - "AcrossIslands"        : All selected or specified primitives (using ##IDs##) that have their opposite part in a different island will be welded
		                 - "AcrossOrSelfIslands"        : All selected or specified primitives (using ##IDs##) that have their opposite part in a different island and also the ones that have their opposite part both in the same island will be welded
		
		PARAMETER       : MaxDist
		Brief           : Maximum distance in UV space that allows two edge to be welded
		Type            : double
		
		To enable distance check, add this parameter and use a positive or zero value.
		
		
		
		"""
		return self.rizomuv.Execute('Weld', p)

	def ResetTo3d(self, p):
		"""
		Copy 3D coordinates to UVW space
		
		PARAMETER       : WorkingSet
		Brief           : The island set on which the task will be applied
		Type            : string
		Default         : "Visible&UnLocked"
		Possible Values :
		                 - Visible
		                 - Selected
		                 - Flat
		                 - NotFlat
		
		Remark: Combinations are possible like "Visible&Selected&Flat"
		
		
		PARAMETER       : UseIslandSelection
		Brief           : Use island selection as input
		Type            : bool
		
		PARAMETER       : Rescale
		Brief           : Rescale the new UVW so that it will be placed into the unity cube
		Type            : bool
		
		
		"""
		return self.rizomuv.Execute('ResetTo3d', p)

	def Unfold(self, p):
		"""
		Flatten 3d or re-flatten already flattened geometry while minimizing the stretching and distorsions
		
		Several modes are available:
		
		  - Default Mode: Process all islands of the working set specifed by ##WorkingSet##
		
		  - Selection Mode: Process the intersection of the island working set specified by ##WorkingSet## a
		    nd the selection set of the primitive type defined using ##PrimType##. ##ProcessSelection## must
		     be specified
		
		  - IDs Mode: Process islands specified by a island ID list (see ##IDs##). Warning: Works only with 
		    island indexes and not with other primitive types. ##WorkingSet## is ignored in that mode
		
		  - Brush Mode: Process the intersection of the island working set specified by ##WorkingSet## and t
		    he area defined by the union of disks (see ##BrushStroke##). If ##ProcessSelection## is specifie
		    d, the processed set will be the intersection of the previously defined set with the vertex sele
		    ction set. ##ProcessUsingBrushes## must be specified
		
		PARAMETER       : PrimType
		Brief           : The primitivite type used to determine the processed set
		Type            : string
		Default         : "Edge"
		Possible Values :
		                 - "Vertex"
		                 - "Edge"
		                 - "Triangle"
		                 - "Polygon"
		                 - "Island"
		
		PARAMETER       : WorkingSet
		Brief           : The island set on which the task will be applied
		Type            : string
		Default         : "Visible&UnLocked"
		Possible Values :
		                 - "Visible"
		                 - "Selected"
		                 - "Flat"
		                 - "NotFlat"
		
		Remark: Combinations are possible like "Visible&Selected&Flat"
		
		
		PARAMETER       : ProcessSelection
		Brief           : Process the selection set of the primitive type specified by ##PrimType##
		Type            : bool
		
		Remark: This has not influence when ##PrimType## is set to Island
		
		
		PARAMETER       : IDs
		Brief           : Process the set of islands specified by theirs ID
		Type            : ints
		
		Remark: This work only when ##PrimType## is set to Island and ##WorkingSet## is ignored in that mode
		
		
		PARAMETER       : ProcessUsingBrushes
		Brief           : Process the set of islands specified by theirs ID
		Type            : bool
		
		Remark: This work only when ##PrimType## is set to Island and ##WorkingSet## is ignored in that mode
		
		
		PARAMETER       : PinMapName
		Brief           : Use the name specified CDataMap as a pin map
		Type            : string
		
		The CDataMap must be per Vertex type and use a scalar value for each vertex. 0 represents non pinned
		 (free) while 1 represents a completely pinned vertex. For importing maps, use import task
		
		
		PARAMETER       : StopIfZeroMix
		Brief           : Stop in difficult case
		Type            : bool
		
		Disable additionnal optimize iterations if ABF give the convex solution only
		
		
		PARAMETER       : DisableOptimize
		Brief           : Stop in difficult case
		Type            : bool
		
		Disable additonnal optimize iterations if ABF give the convex solution only
		
		
		PARAMETER       : BorderIntersections
		Brief           : Prevent self border intersections
		Type            : bool
		
		If present and true, the unfolding algorithm will prevent the forming of self border intersection fo
		r each island, independently
		
		
		PARAMETER       : TriangleFlips
		Brief           : Prevent triangle flips
		Type            : bool
		
		If present and true, the unfolding algorithm will prevent triangle flips forming
		
		
		PARAMETER       : ExportVertIDs
		Brief           : Exports processed vertex ids in brush mode
		Type            : table
		
		If present, the processed vertexes IDs of the UV space will be exported in ##ProcessedVertIDs##
		
		Remark: This works only in brush mode
		
		
		PARAMETER       : ExportVertIDs.UseImportedPolygonUVW
		Brief           : Converts processed vertex ids to be conform to the imported UVW polygons
		Type            : bool
		
		This is useful when the imported mesh contain topology errors and when it the host application doesn
		't handle UVW mesh topology modifications
		
		Remark: This option enable ##ExportVertIDs##
		
		
		PARAMETER       : Mix
		Brief           : Operation Mix
		Type            : double
		Default         : 1.0
		
		Value should be in range [0...1]. Should be used for already flattened geometry. 0 for no effect, 1 
		for maximal effect
		
		
		PARAMETER       : Iterations
		Brief           : Number of iterations of the Optimize algorithm applied after the unfolding process
		Type            : int
		
		Remark: Negative values will disable the Optimize algorithm. In that case all constraints are ignore
		        d
		
		Remark: Value 0 does not disable the optimization in all cases since when the unfolding encounter bo
		        rder intersection or triangle flips, some Optimize iterations may be added
		
		
		PARAMETER       : RoomSpace
		Brief           : Minimum space allowed between borders for the self border intersection preventing algorithm
		Type            : double
		Default         : 0.0
		
		The value is in UVW space unit
		
		Remark: Care should be taken when setting that value. Meaningfull values should be the same order of
		         the inverse of the final texture map resolution multiplied by the size of its support in th
		        e UV space. Too big values can increase a lot the process time and even give strange results
		         in some cases
		
		Remark: This has no effect if ##BorderIntersections## is disabled
		
		
		PARAMETER       : MinAngle
		Brief           : Minimum angle when computing data
		Type            : double
		Default         : 0.00001
		
		This minimal value protect transcendantal functions. You should not change that value unless you mad
		e serious tests that shows better quality results. On the contrary case, let it as its default
		
		
		PARAMETER       : FreeSelectionBorders
		Brief           : Free vertexes selection set's border vertexes
		Type            : bool
		
		When disabled, the vertexes located on a vertex selection set border are automatically pinned (so th
		at they don't move). This is the expected behavior. However in some special use cases, it can be use
		ful to let those vertex move freely, which can be done by enabling this parameter
		
		
		PARAMETER       : FillHoles
		Brief           : Fill island's holes
		Type            : bool
		
		If enabled (present and true), islands holes will be filled by temporally polygons. This make the ho
		les rigid and can help to produce better results in some use cases
		
		
		OUTPUT      : ProcessedVertIDs
		Brief           : Processed vertex ids when ##ProcessUsingBrushes## is enabled
		Type            : ints
		
		OUTPUT      : BijectionFailedIslandIDs
		Brief           : Island indexes of the islands incorrectly unfolded
		Type            : ints
		
		PARAMETER       : ProcessAllIfNoneSelected
		Brief           : Process all if the selection corresponding to ##PrimType## is empty
		Type            : bool
		
		PARAMETER       : BrushStroke
		Brief           : Table containing a list of brushes (see data of type Brush)
		Type            : table
		
		
		"""
		return self.rizomuv.Execute('Unfold', p)

	def SymmetrySet(self, p):
		"""
		Set symmetry plane parameters
		"""
		return self.rizomuv.Execute('SymmetrySet', p)

	def Constrain(self, p):
		"""
		Add constraints to edges or vertexes
		
		Remark: Theses constraints will have impact on Optimize and Unfold tasks
		
		PARAMETER       : PrimType
		Brief           : The primitive type used to determine the processed set
		Type            : string
		Default         : "Edge"
		Possible Values :
		                 - "Vertex"
		                 - "Edge"
		                 - "Triangle"
		                 - "Polygon"
		                 - "Island"
		
		PARAMETER       : WorkingSet
		Brief           : The island set on which the task will be applied
		Type            : string
		Default         : "Visible&UnLocked"
		Possible Values :
		                 - "Visible"
		                 - "Selected"
		                 - "Flat"
		                 - "NotFlat"
		
		Remark: Combinations are possible like "Visible&Selected&Flat"
		
		
		PARAMETER       : Mode
		Brief           : 
		Type            : string
		Default         : "Pin"
		Possible Values :
		                 - "Pin"        : Pin selected vertexes
		                 - "UnPin"        : UnPin selected vertexes
		                 - "Hinge"        : Add hinge to selected vertexes
		                 - "UnHinge"        : Remove hinge to selected vertexes
		                 - "EdgeH"        : Add horizontal constraint to selected edges
		                 - "EdgeV"        : Add vertical constraint to selected edges
		                 - "EdgeA"        : Add alignement constraint to selected edges
		                 - "UnConstrainEdge"        : Unconstrain selected edges
		                 - "UnConstrainAllEdges"        : Unconstrain all edges
		
		Remark: Adding the constraints doesn't move any UV vertexes. If you want to update the flattened geo
		        metry according to  new constraints, you have to execute an Unfold or Optimize task
		
		Remark: Hinge constraints has effect only when alignement constraints are added to the edges connect
		        ed to the vertex.
		
		
		
		"""
		return self.rizomuv.Execute('Constrain', p)

	def Undo(self, p):
		"""
		Undo last command
		"""
		return self.rizomuv.Execute('Undo', p)

	def Redo(self, p):
		"""
		Redo undoed command
		"""
		return self.rizomuv.Execute('Redo', p)

	def Optimize(self, p):
		"""
		Deform the geometry to reduce stretching
		
		Several mode are available:
		
		  - Default Mode: Process all islands of the working set specifed by ##WorkingSet##
		
		  - Selection Mode: Process the intersection of the island working set specified by ##WorkingSet## a
		    nd the selection set of the primitive type defined using ##PrimType##. ##ProcessSelection## must
		     be specified
		
		  - IDs Mode: Process islands specified by a island ID list (see ##IDs##). Warning: Works only with 
		    island indexes and not with other primitive types. ##WorkingSet## is ignored in that mode
		
		  - Brush Mode: Process the intersection of the island working set specified by ##WorkingSet## and t
		    he area defined by the union of disks (see ##BrushStroke##). If ##ProcessSelection## is specifie
		    d, the processed set will be the intersection of the previously defined set with the vertex sele
		    ction set. ##ProcessUsingBrushes## must be specified
		
		PARAMETER       : PrimType
		Brief           : The primitivite type used to determine the processed set
		Type            : string
		Default         : "Edge"
		Possible Values :
		                 - Vertex
		                 - Edge
		                 - Triangle
		                 - Polygon
		                 - Island
		
		PARAMETER       : WorkingSet
		Brief           : The island set on which the task will be applied
		Type            : string
		Default         : "Visible&UnLocked"
		Possible Values :
		                 - Visible
		                 - Selected
		                 - Flat
		                 - NotFlat
		
		Remark: Combinations are possible like "Visible&Selected&Flat"
		
		Remark: Value "NotFlat" doesn't generate errors but nothing will be processed as the algorithm can p
		        rocess flat islands only
		
		
		PARAMETER       : ProcessSelection
		Brief           : Process the selection set of the primitive type specified by ##PrimType##
		Type            : bool
		
		Remark: This has not influence when ##PrimType## is set to Island
		
		
		PARAMETER       : ProcessJustCut
		Brief           : Process islands that has been just cut ( and not edited since )
		Type            : bool
		
		PARAMETER       : IDs
		Brief           : Process the set of islands specified by theirs ID
		Type            : ints
		
		Remark: This work only when ##PrimType## is set to Island and ##WorkingSet## is ignored in that mode
		
		
		PARAMETER       : ProcessUsingBrushes
		Brief           : Process the set of islands specified by theirs ID
		Type            : bool
		
		Remark: This work only when ##PrimType## is set to Island and ##WorkingSet## is ignored in that mode
		
		
		PARAMETER       : PinMapName
		Brief           : Use the name specified CDataMap as a pin map
		Type            : string
		
		The CDataMap must be per Vertex type and use a scalar value for each vertex. 0 represents non pinned
		 (free) while 1 represents a completely pinned vertex. For importing maps, use import task
		
		
		PARAMETER       : BorderIntersections
		Brief           : Prevent self border intersections
		Type            : bool
		
		If present and true, the OPTIMIZEing algorithm will prevent the forming of self border intersection 
		for each island, independently
		
		
		PARAMETER       : TriangleFlips
		Brief           : Prevent triangle flips
		Type            : bool
		
		If present and true, the OPTIMIZEing algorithm will prevent triangle flips forming
		
		
		PARAMETER       : ExportVertIDs
		Brief           : Exports processed vertex ids in brush mode
		Type            : table
		
		If present, the processed vertexes IDs of the UV space will be exported in ##ProcessedVertIDs##
		
		Remark: This works only in brush mode
		
		
		PARAMETER       : ExportVertIDs.UseImportedPolygonUVW
		Brief           : Converts processed vertex ids to be conform to the imported UVW polygons
		Type            : bool
		
		This is useful when the imported mesh contain topology errors and when it the host application doesn
		't handle UVW mesh topology modifications
		
		Remark: This option implicitly enable ##ExportVertIDs## as well
		
		
		PARAMETER       : Mix
		Brief           : Operation Mix
		Type            : double
		Default         : 1.0
		
		Value should be in range [0...1]. 0 for no effect, 1 for maximal effect
		
		
		PARAMETER       : AngleDistanceMix
		Brief           : Mix between conservation of angles or distances
		Type            : double
		Default         : 1.0
		
		0 for angle conservation, 1 for distances conservation
		
		
		PARAMETER       : KeepMetric
		Brief           : Keep area from 3D space to UV space
		Type            : bool
		
		When not present (disabled), the processed areas will keep their current area. When enabled, they wi
		ll be scaled so that their final areas will match their original 3D space areas
		
		
		PARAMETER       : Iterations
		Brief           : Number of iterations
		Type            : int
		
		Remark: Negative values will disable the Optimize algorithm. In that case all constraints are ignore
		        d
		
		Remark: Value 0 does not disable the optimization in all cases since when the unfolding encounter bo
		        rder intersection or triangle flips, some Optimize iterations may be added
		
		
		PARAMETER       : RoomSpace
		Brief           : Minimum space allowed between borders for the self border intersection preventing algorithm
		Type            : double
		Default         : 0.0
		
		The value is in UVW space unit
		
		Remark: Care should be taken when setting that value. Meaningfull values should be the same order of
		         the inverse of the final texture map resolution multiplied by the size of its support in th
		        e UV space. Too big values can increase a lot the process time and even give strange results
		         in certain cases. 
		
		Remark: This has no effect if ##BorderIntersections## is disabled
		
		
		PARAMETER       : MinAngle
		Brief           : Minimum angle when computing data
		Type            : double
		Default         : 0.00001
		
		This minimal value protect transcendantal functions. You should not change that value unless you mad
		e serious tests that shows better quality results. On the contrary case, let it as its default
		
		
		PARAMETER       : FreeSelectionBorders
		Brief           : Free vertexes selection set's border vertexes
		Type            : bool
		
		When disabled, the vertexes located on a vertex selection set border are automatically pinned (so th
		at they don't move). This is the expected behavior. However in some special use cases, it can be use
		ful to let those vertex move freely, which can be done by enabling this parameter
		
		
		PARAMETER       : FillHoles
		Brief           : Fill island's holes
		Type            : bool
		
		If enabled (present and true), islands holes will be filled by temporally polygons. This make the ho
		les rigid and can help to produce better results in some use cases
		
		
		OUTPUT      : ProcessedVertIDs
		Brief           : Processed vertex ids when ##ProcessUsingBrushes## is enabled
		Type            : ints
		
		PARAMETER       : ProcessAllIfNoneSelected
		Brief           : Process all if the selection corresponding to ##PrimType## is empty
		Type            : bool
		
		PARAMETER       : BrushStroke
		Brief           : Table containing a list of brushes
		Type            : table
		
		
		"""
		return self.rizomuv.Execute('Optimize', p)

	def Pack(self, p):
		"""
		Transform islands into UV space to fill the available space smartly
		
		Scale, rotate and translate islands and groups of island so that they fit in a rectangular area that
		 is as small as possible. The resulting W/H rectangular space ratio will be as close as possible to 
		the one given by the user (usually 1:1)
		
		For each active tile present in the group hierarchy (the default group hierarchy is "RootGroup"):
		
		  1. Determine the working set of islands (and island groups) using ##WorkingSet##. If the working s
		    et restricts to the selected island selection set, the selected islands will be transformed and
		     the unselected islands will be considered as locked so that they constitute the forbidden area
		
		  2. Rescale the unlocked islands or island groups using the setting in ##ScalingMode##
		
		  3. Re orient the unlocked islands or island groups using the settings in ##Rotate.Mode##
		
		  4. Translate (and also rotates if Rotate.Step != 0.0) the unlocked islands or island group to fit 
		    them all  inside the given "Box" minus the "Margin". If the island set is to big the given Box 
		    will be grown, keeping its H/W ratio as much as possible
		
		  5. Post process: Globaly rescales *all islands* using the settings in ##LayoutScalingMode## to fit
		     the whole working set inside the given box/tile geometry and position. This last point is done
		     only if ##LayoutScalingMode## is set to "Best fit" or "Force Fit"
		
		Most of the packing parameters must be specified using the ##PackElemProperties## structure and can 
		be included into ##Global##. When ##Global## is specified, its values will be used for all elements 
		(islands, group and tiles).
		
		To specify specific values to specific elements, use the task ##IslandProperties## or task ##IslandG
		roup##. Specifying theses parameters will override the default values (but not the ones specified in
		 ##Global## as ##Global## as top priority)
		
		Values can also be attached to the "RootGroup". So the evaluation priority follows this order:
		
		  1. Parameters contained in the ##Global## parameter structure	           , if not found,
		
		  2. Parameters contained in an Island, Group or Tile                         , if not found,
		
		  3. Parameters contained in the root group hierarchy (Default is "RootGroup"), if not found,
		
		  4. Internal default values of the packing algorithm's code
		
		Remark: Some parameters have meaning for island group (G) and tiles (T), some others have meaning on
		        ly for island (I) and group, some others for tile only. Look at the beginning of each parame
		        ter's text help to see which element, (I), (G) or (T) they have an influence
		
		Remark: The user has to give a 2D box (see Box parameter). However only the lower left corner and th
		        e W/H ratio will be used to set the position and set the scale of the final rectangular boun
		        ding box  containing all the involved islands and group of islands. However the complete geo
		        metry of that bounding box is used if "layout post scaling" is applied (see ##LayoutScalingM
		        ode## parameter).
		
		PARAMETER       : RootGroup
		Brief           : Root group name
		Type            : string
		Default         : "RootGroup"
		
		Root group name of the group that constitutes the base of the island group hierarchy to be packed. T
		he default value should work for simple cases
		
		
		PARAMETER       : AuxGroup
		Brief           : Auxiliary group name
		Type            : string
		
		If specified, elements contained in that group will be added when packing tiles. Elements are added 
		if the can fit. If they fit, they will be transfered from that group to the processed tile(s)
		
		
		PARAMETER       : WorkingSet
		Brief           : The island set on which the task will be applied
		Type            : string
		Default         : "Visible"
		Possible Values :
		                 - "Visible"
		                 - "Selected"
		                 - "Flat"
		                 - "NotFlat"
		
		Remark: Combinations are possible like "Visible&Selected&Flat"
		
		
		PARAMETER       : PostLayoutScalingProcessIslandSelection
		Brief           : Process island and island group selection for the post layout scaling operations
		Type            : bool
		
		If false or not present all visible elements will be processed
		
		
		PARAMETER       : ProcessTileSelection
		Brief           : Process tile selection
		Type            : bool
		Default         : false
		
		If false all tiles will be processed
		
		
		PARAMETER       : Translate
		Brief           : Enable island translation (the main packing algorithm)
		Type            : bool
		
		Remark: MUST BE EXPLICITLY ENABLED. If not specfied, the islands will not be translated
		
		Remark: If island translation is disabled the post scaling operation is still active.
		
		
		PARAMETER       : Global
		Brief           : Packing parameters
		Type            : table
		
		Use CPackElemProperties to specify theses parameters
		
		Remark: These parameter can be specified for each packed elements (island or group or tile)
		
		
		PARAMETER       : RecursionDepth
		Brief           : Recursion depth
		Type            : int
		Default         : 1
		
		If enabled the leaf groups of the group hierarchy will packed first using their own bounding box rat
		io. Then the parents of those groups will be packed also in the same manner and so on until the root
		 group
		
		The integer value specifies the recursion depth:
		
		  - 0 means that it will pack the content of the group specified by ##RootGroup##
		
		  - 1 means that it will pack the content of the group specified by ##RootGroup## and its children
		
		  - 2 means that it will pack the content of the group specified by ##RootGroup## and its children a
		    nd its grand children
		
		  - etc..
		
		Remark: if "RootGroup" is the default RootGroup specifying 0 will result in nothing since the defaul
		        t RootGroup contains only Tiles. So if "RootGroup" is the default root group the default val
		        ue should be one 1, so that the content of the tiles will be packed
		
		
		PARAMETER       : PaddingSize
		Brief           : Padding between each island (or group) in real UVW unit. For (I) and (G)
		Type            : double
		
		Room let between each island (or group) in real UVW unit
		
		  - Higher values will decrease significantly the process time
		
		  - The process time is roughly inversely proportional to that value + 1
		
		Remark: In order to have a padding size in pixel, provide the following value: PaddingInPixels / Res
		        olution * givenBoxWidth
		
		
		PARAMETER       : MarginSize
		Brief           : Padding on top/left/right/bottom of the tiles in real UVW unit. For (T) only.
		Type            : double
		
		PARAMETER       : MapResolution
		Brief           : Final texture map resolution. For (T)
		Type            : int
		
		Should not be inferior to ##Resolution##
		
		Not used by the algorithm itself but used to store user texture map's resolution in the standalone.
		
		
		PARAMETER       : Resolution
		Brief           : Algorithm's resolution, in pixels. For (T) and (G)
		Type            : int
		
		If this parameter is specified, the value of ##Accuracy## will be ignored and the actual accuracy us
		ed for the packing algorithm will be computed using ##Resolution## and the total island area to pack
		 in UV space.
		
		When the maximum size of the shells are not know in advance (like when their size can exceed the siz
		e of the tile), it is safer to specify the algorithm precision using that parameter instead of using
		 ##Accuracy##. Using ##Resolution## give a better control on the processing time
		
		
		PARAMETER       : Accuracy
		Brief           : Horizontal accuracy of the packing algorithm in real UVW unit. For (T) and (G)
		Type            : double
		
		  - Low values give better placements but the process is slower
		
		  - Computation time is linear over the inverse of that parameter
		
		Remark: Using small values (high precision) with very big shells will make the packing process very 
		        long. If in the application context, the size of the islands to pack are not bounded and/or 
		        not know in advance, it is preferable to specify the quality of the packing using ##Resoluti
		        on## instead of that parameter
		
		Remark: Even if the accuracy is very coarse, the algorithm will never create overlaps. However some 
		        space will be wasted
		
		Remark: To obtain good performance, when the wanted Accuracy is inferior to PaddingSize it is strong
		        ly recommended to put the same value of PaddingSize for Accuracy: if (PaddingSize > Accuracy
		        ) Accuracy = PaddingSize; This will not result in a significant lost of space and can greatl
		        y improve the processing time
		
		
		PARAMETER       : MaxMutations
		Brief           : Maximum trials. For (T) and (G)
		Type            : int
		
		Mutation can be seen as iterations. The more iterations are done, the more chance there will be to f
		ind a good island ordering placement, so that the available area is well used.
		
		Remark: The final computation time is O(n) toward this parameter
		
		Remark: The more the island count is great (> 5000), the less this parameter has an influence. This 
		        is especially true is all island have roughly the same size in UV space
		
		
		Brief           : Packing island rotation mode. For (I) and (G)
		Type            : 
		Possible Values :
		                 - E_PACK_ROTATE_MODE_OFF        : Disabled (Leave the current island's orientation)
		                 - E_PACK_ROTATE_MODE_HORIZONTAL        : Pre-orient the island horizontally before packing (using its minimal bounding box as reference)
		                 - E_PACK_ROTATE_MODE_VERTICAL        : Pre-orient the island vertically before packing (using its minimal bounding box as reeference)
		                 - E_PACK_ROTATE_MODE_X2V        : Pre-orient the island so that it X axis in 3D space be aligned to the V axis in UV Space
		                 - E_PACK_ROTATE_MODE_Y2V        : Pre-orient the island so that it Y axis in 3D space be aligned to the V axis in UV Space
		                 - E_PACK_ROTATE_MODE_Z2V        : Pre-orient the island so that it Z axis in 3D space be aligned to the V axis in UV Space
		
		Before packing the islands can be re oriented in a pre-process phase.
		
		Remark: if E_PACK_ROTATE_MODE_OFF is selected and if ##Rotate.Step## != 0, the islands will be rotat
		        ed in the packing stage. (This is because the orientation optimization is enabled when ##Rot
		        ate.Step## is present and != 0.0)
		
		
		PARAMETER       : Rotate.Mode
		Brief           : Rotation mode. For (I)
		Type            : int
		
		PARAMETER       : Rotate.Min
		Brief           : Rotation applied in the pre-process stage in degrees. For (I) and (G)
		Type            : double
		
		Remark: Is also the first rotation step angle of the orientation optimization
		
		
		PARAMETER       : Rotate.Max
		Brief           : Rotation max in degree. For (I) and (G)
		Type            : double
		
		PARAMETER       : Rotate.Step
		Brief           : Rotation step for the optimization of island orientation in degrees. For (I) and (G)
		Type            : double
		
		Remark: Value 0 will disable the optimization
		
		Remark: The process time is proportional to 1/Rotate.Step. So a small value will augment considerabl
		        y the process time
		
		
		Brief           : Pack scaling modes
		Type            : 
		Possible Values :
		                 - E_PACK_SCALING_MODE_OFF        : Disabled. Do not rescale the islands (WARNING: if global scaling mode is enabled T_PACK_UVLAYOUT_SCALING, the island can be scaled in the post process)
		                 - E_PACK_SCALING_MODE_SET_3D_AREA        : Scale each island so that it will have the same area it has in 3D space
		                 - E_PACK_SCALING_MODE_AVG_RATIO_OF_MOVABLE_ISLANDS        : Scale each island so that its UV/3D ratio will have the average ratio of the movable island set ratio.
		                 - E_PACK_SCALING_MODE_AVG_RATIO_OF_GROUP        : Scale each island so that its UV/3D ratio will have the average ratio of the island group set ratio.
		                 - E_PACK_SCALING_MODE_AVG_RATIO_OF_FIXED_ISLANDS        : Scale each island so that its UV/3D ratio will have the average ratio of the island group set minus the set of movable islands (fixed islands)
		                 - E_PACK_SCALING_MODE_AVG_RATIO_OF_ALL_ISLANDS        : Scale each island so that its UV/3D ratio will have the average ratio of all islands of the full mesh without taking account any selection/visible/locked and groups flags
		                 - E_PACK_SCALING_MODE_AVG_RATIO_USER_SPECIFIED        : Scale each island using a ratio specified by ##Scaling.SpecifiedScale##
		                 - E_PACK_SCALING_MODE_TEXEL_DENSITY        : Scale each island so that it fit the texel density specified by ##Scaling.TexelDensity##
		
		PARAMETER       : Scaling.Mode
		Brief           : Island scaling mode. For (T) and (G)
		Type            : int
		
		Control how the unlocked islands will be rescaled (or not) at pre-process stage
		
		With E_PACK_SCALING_MODE_KEEP_ACTIVE_UV_AREA and E_PACK_SCALING_MODE_KEEP_TOTAL_UV_AREA, the purpose
		 is to give a equal scale ratio between 3D space and UV space for the movable (not fixed) islands. E
		ach island i is given a rescale s_i value
		
		        s_i = sqrt( (A3D_i / Auv_i) * (Auv / A3D) )
		
		where
		
		  - Auv_i (resp A3D_i) is the island's i area in UV (resp 3D) space
		
		  - Auv   (resp A3D) is the UV (resp 3D) area of the MOVABLE set islands, or the GROUP set, or the F
		    IXED set of islands or the TOTAL set of islands, depending of E_PACK_SCALING_MODES
		
		Remark: CG applications should use E_PACK_SCALING_MODE_OFF to keep the islands at their current size
		        . However after a first unfolding using that API, the islands usually have incorrect size, s
		        o it it may be preferable to use E_PACK_SCALING_MODE_AVG_RATIO_OF_GROUP mode in those cases.
		
		Remark: CAD applications may use E_PACK_SCALING_MODE_SET_3D_AREA to obtain islands in UV space that 
		        have the same size in 3D Space (the area will be the same). However if user are allowed to m
		        anually rescale islands or if they don't want to be island rescaled for other reason they ma
		        y use also E_PACK_SCALING_MODE_OFF
		
		
		PARAMETER       : Scaling.Min
		Brief           : Minimum value of the scaling factor when optimizing islands scale
		Type            : double
		
		PARAMETER       : Scaling.Max
		Brief           : Maximum value of the scaling factor when optimizing islands scale
		Type            : double
		
		PARAMETER       : Scaling.SpecifiedScale
		Brief           : Scale value for all islands.
		Type            : double
		
		Remark: ##Scaling.Mode## must be set to E_PACK_SCALING_MODE_AVG_RATIO_USER_SPECIFIED for this option
		         to work
		
		About the scaling factor and texel density. With a SQUARE tile and a SQUARE texture map:
		
		        TD = (lenUV / len3D) * (mapRez / tileSize)
		
		where:
		
		  - TD is the wanted texel density in texel per meter in 3D space
		
		  - lenUV is a length of a given element in UV space (for example an edge)
		
		  - len3D is the length of the SAME element in 3D space (the same edge)
		
		  - mapRez is the horizontal resolution of the texture map
		
		  - tileSize is the horizontal size of the tile in meter
		
		The SDK defines T_PACK_SCALING_SPECIFIED_SCALE as the ratio lenUV / len3D, so
		
		        ##Scaling.SpecifiedScale## = TD * tileSize / maprez
		
		TD is what should be displayed to users in texel per meter
		
		
		PARAMETER       : Scaling.TexelDensity
		Brief           : Targeted texel density value for all islands. Can be added to the root group (T)
		Type            : double
		
		Remark: ##Scaling.Mode## must be set to E_PACK_SCALING_MODE_TEXEL_DENSITY for this option to work
		
		Remark: ##MapResolution## must also be specified for this option to work
		
		Remark: The value of Scene.Setting.Unit will be used to determine the TD units.
		
		The texel density is defined as the following. With a SQUARE tile and a SQUARE texture map:
		
		        TD = (lenUV / len3D) * (mapRez / tileSize)
		
		where:
		
		  - TD is the wanted texel density in texel per unit in 3D space. Unit is determined by the value of
		     "Scene.Setting.Unit"
		
		  - lenUV is a length of a given element in UV space (for example an edge)
		
		  - len3D is the length of the SAME element in 3D space (the same edge)
		
		  - mapRez is the horizontal resolution of the texture map that can be specified using ##MapResoluti
		    on## or added using an ##PackElemProperties## object added to the Root Group
		
		  - tileSize is the horizontal size of the tile present in the 2D box "Mesh.RootGroup.Properties.Box
		    ". The unit is determined by the value of "Scene.Setting.Unit"
		
		
		PARAMETER       : Scaling.Mix
		Brief           : Allow distinct scaling in the same tile or group
		Type            : bool
		
		Enabling this parameter creates layouts with better UV area usage when distinct values of scaling ar
		e acceptable. Island or groups are scaled down if they are bigger than their tile's or group's frame
		. The ##Scaling.Min## value must be compatible to the necessary scaling down. 
		
		
		Brief           : Post layout scaling modes
		Type            : 
		Possible Values :
		                 - E_PACK_LAYOUT_SCALING_MODE_DISABLED        : Do nothing. Leave the islands at their current position and scale. This option must be selected if the locked islands/groups must stay at their current position.
		                 - E_PACK_LAYOUT_SCALING_MODE_TRANSLATE_ONLY        : No post scaling, however the bounding box of the involved island set will be translated so that its lower left corner will match the lower left corner of the specified box/tile. This is useless most of the time if used after a packing task since the islands are firstly positioned on the low left side
		                 - E_PACK_LAYOUT_SCALING_MODE_BEST_FIT        : Scale all islands so that their global bbox fit best the given box. The scaling will be uniform: same scaling for U and V axis
		                 - E_PACK_LAYOUT_SCALING_MODE_FORCE_FIT        : Scale all islands so that their global bbox fit completely the given box. The scaling will be non uniform: Scaling in U and V axis can be different
		
		PARAMETER       : LayoutScalingMode
		Brief           : Post layout scaling mode. For (T) and (G)
		Type            : int
		
		After the islands be transformed by the main packing algorithm, all involved islands can be scaled a
		nd repositioned uniformly as a post-process step using ##LayoutScalingMode##. In that case all islan
		ds will receive the same global transformation as if they where an unique tight mesh.
		
		Remark: If ##LayoutScalingMode## != E_PACK_LAYOUT_SCALING_MODE_DISABLED even the locked islands will
		         be translated and rescaled
		
		
		OUTPUT      : Coverages
		Brief           : Coverage for each squares involved during the packing task
		Type            : doubles
		
		The coverage values are organised as following [ u0v0 u1v0 u2v0 u0v1 u1v1 u1v1]. All of them are usu
		ally between 0 and 1, but can be superior to 1 in case of the presence of stacked islands or more ge
		nerally when islands overlap.
		
		
		PARAMETER       : ProcessIslandSelection
		Brief           : Process island and island group selection
		Type            : bool
		
		
		"""
		return self.rizomuv.Execute('Pack', p)

	def Select(self, p):
		"""
		Change the selection flag properties of elements using various methods.
		
		For each primitive type, only a single mode among the listed ones must be specified.
		
		When ##PrimType## == "Vertex":
		
		##All##
		##List##
		##ShortestPath##
		##HightLighted##
		##PyramidalFrustrum##
		##Grow##
		##Shrink##
		##PolyGroups##
		##SmoothGroups##
		##Materials##
		##Objects##
		##Border##
		When ##PrimType## == "Edge":
		
		##All##
		##List##
		##Loop##
		##ShortestPath##
		##HightLighted##
		##Arc##
		##Parallel##
		##ConvertSource##
		##PyramidalFrustrum##
		##Border##
		##PolyGroups##
		##SmoothGroups##
		##Materials##
		##Objects##
		##Grow##
		##Shrink##
		##Auto##
		When ##PrimType## == "Triangle":
		
		##All##
		##List##
		##PyramidalFrustrum##
		##Border##
		##PolyGroups##
		##SmoothGroups##
		##Materials##
		##Objects##
		##Grow##
		##Shrink##
		When ##PrimType## == "Polygon":
		
		##All##
		##List##
		##PyramidalFrustrum##
		##PolyGroups##
		##SmoothGroups##
		##Materials##
		##Objects##
		##Element##
		##Grow##
		##Shrink##
		##InvertedNormals##
		##Overlaps##
		When ##PrimType## == "Island":
		
		##All##
		##List##
		##PyramidalFrustrum##
		##PolyGroups##
		##SmoothGroups##
		##Materials##
		##Objects##
		##Element##
		##InvertedNormals##
		##Overlaps##
		When ##PrimType## == "IslandGroup":
		
		##All##
		##Names##
		##PyramidalFrustrum##
		##IslandGroupMode##
		PARAMETER       : PrimType
		Brief           : The primitive type that you want to select/deselect
		Type            : string
		Default         : "Edge"
		Possible Values :
		                 - Vertex
		                 - Edge
		                 - Triangle
		                 - Polygon
		                 - Island
		                 - IslandGroup
		
		PARAMETER       : WorkingSet
		Brief           : The island set on which the task will be applied
		Type            : string
		Default         : "Visible"
		Possible Values :
		                 - Visible
		                 - Selected
		                 - Flat
		                 - NotFlat
		
		Remark: Combinations are possible like "Visible&Selected&Flat"
		
		
		PARAMETER       : Select
		Brief           : Select mode (Add)
		Type            : bool
		
		PARAMETER       : DeSelect
		Brief           : Deselection mode
		Type            : bool
		
		PARAMETER       : Mirror
		Brief           : Mirror current selection
		Type            : bool
		
		PARAMETER       : IDs
		Brief           : Input primitives indexes used for some modes of this selection task
		Type            : ints
		
		PARAMETER       : ResetBefore
		Brief           : Reset the selection before doing anything else
		Type            : bool
		
		PARAMETER       : XYZSpace
		Brief           : Use 3D space coordinates for algorithms
		Type            : bool
		
		PARAMETER       : IslandGroupMode
		Brief           : Tell if both tiles and regular island group must be selected or deselected
		Type            : string
		Default         : "Group"
		Possible Values :
		                 - Tile
		                 - Group
		                 - Both
		
		Remark: It has an effect only if ##PrimType##=="IslandGroup"
		
		Remark: Ignored is ##Names## is specified as input
		
		
		PARAMETER       : InterpretIDsUsingOriginalUVWPolys
		Brief           : Interpret the vertex IDs list as original imported polygon UVW connectivity instead of the corrected one
		Type            : bool
		
		It means that if the UVW space connectivity mesh has been internally modified (repaired at import, o
		r by subsequent cut/weld operation) the command will correctly select all newly created vertex ids u
		sing a built indexing table made with original UVW polygons and the current ones
		
		Remark: PrimType must be set to "Vertex" mode only
		
		
		PARAMETER       : EdgesAsPolyEdgeIDs
		Brief           :  Understand IDs list as list of edges references defined using couples of polygon IDs and polygon side IDs
		Type            : bool
		
		The ##IDs## list should be filled like this [PolyID0, PolySideID0, PolyID1, PolySideID1 ... PolyIDN,
		 PolySideIDN
		
		
		PARAMETER       : Selected
		Brief           : Use the current selection as input for "Loop" tool or "Parallel" tool
		Type            : bool
		
		PARAMETER       : ProtectMapName
		Brief           : Protect map name
		Type            : string
		
		Set to 1 for maximum protection, -1 for attraction, 0 for neutral.
		
		Remark: Currently taken into account by ##Auto.QuasiDevelopable## and ##Auto.Skeleton##
		
		
		PARAMETER       : Names
		Brief           : Primitives names used for some modes of the selection
		Type            : strings
		
		Remark: Used only for island group selection at the moment
		
		
		PARAMETER       : Paths
		Brief           : Select island groups using their paths
		Type            : strings
		
		Remark: The root group path must be not be included, by default it's "RootGroup"
		
		
		PARAMETER       : Null
		Brief           : No selection action
		Type            : bool
		
		This can be used to trigger the task without actually doing anything for some reasons
		
		
		PARAMETER       : All
		Brief           : Select all primitives
		Type            : bool
		
		PARAMETER       : List
		Brief           : Select primitives contained in the list ##IDs##
		Type            : bool
		
		Remark: In case of island group selection the ##Names## string list members will be used instead of 
		        the indexes of ##IDs##.
		
		
		PARAMETER       : ShortestPath.StartID
		Brief           : Start edgeID of the shortest path tool
		Type            : int
		
		Remark: Avaible only when ##PrimType## == "Edge"
		
		Remark: Specify -1 to use the last highlighted edge
		
		
		PARAMETER       : ShortestPath.EndID
		Brief           : End edgeID of the shortest path tool
		Type            : int
		
		PARAMETER       : PolyArea
		Brief           : Select polygons by geometrical properties, comparing their normals
		Type            : table
		
		All polygons that have their normal making an angle inferior to the specified value will be selected
		
		
		PARAMETER       : PolyArea.AbsoluteAngle
		Brief           : Maximum absolute angle between the connected polygons around the polygons seeds specified in ##IDs##
		Type            : double
		
		All polygons that have their normal making an angle inferior to the specified value will be selected
		
		
		PARAMETER       : PolyArea.RelativeAngle
		Brief           : Maximum relative angle between two connected triangles
		Type            : double
		
		It will extends the selection starting from the polygon seeds specified in ##IDs##
		
		
		PARAMETER       : PolyArea.UseGeoNormals
		Brief           : Use geo normals instead of model file's user normals 
		Type            : bool
		
		This has an effect only for the relative angle tests. Absolute tests always use geo normals.
		
		
		PARAMETER       : PolyArea.AccrossSeams
		Brief           : Progate the selection accross island's seams
		Type            : bool
		
		PARAMETER       : PolyArea.SmoothMix
		Brief           : Smooth mesh mix value applied prior to selecting the polygons
		Type            : double
		
		The value must be between 0.0 and 1.0
		
		
		PARAMETER       : PolyArea.SmoothIterations
		Brief           : Smooth mesh iteration count applied prior to selecting the polygons (default is 2)
		Type            : int
		
		PARAMETER       : PolyArea.MaxGapSize
		Brief           : Fill non selected polygons sourrounded by selected polygons
		Type            : int
		
		If a non selected group of of connected polygons is smaller than the specified value, it will be add
		ed to the selection
		
		
		PARAMETER       : InvertedNormals
		Brief           : Select islands or polygons that has negative area
		Type            : bool
		
		Remark: Avaible only when ##PrimType## == "Polygon" or ##PrimType## == "Island"
		
		
		PARAMETER       : Overlaps
		Brief           : Select islands or polygons that has some overlaps with others, either in the same island or accross islands
		Type            : bool
		
		Remark: Avaible only when ##PrimType## == "Polygon" or ##PrimType## == "Island"
		
		
		PARAMETER       : Loop
		Brief           : Edge or Polygon loop propagation algorithm
		Type            : table
		
		In case ##PrimType## == "Edge" the propagation starts from the edge(s) specified in ##IDs##
		
		In case ##PrimType## == "Poly" the propagation starts also from the edge(s) specified in ##IDs## but
		 select polygons
		
		Remark: Avaible only when ##PrimType## == "Edge" or ##PrimType## == "Poly"
		
		
		PARAMETER       : Loop.MaxNum
		Brief           : Max number of edge selected for the loop tool
		Type            : int
		Default         : 9999
		
		Remark: The pameter presence determines the limit is active
		
		
		PARAMETER       : Loop.MaxAngle
		Brief           : Max angle between two consecutive edges allowed while propagating selection for the loop tool
		Type            : double
		Default         : 180.0
		
		Remark: The pameter presence determines the limit is active
		
		
		PARAMETER       : Loop.GeometryBased
		Brief           : Use geometry instead of topology to determine the propagation direction
		Type            : bool
		
		PARAMETER       : Loop.StopAtSelection
		Brief           : Stop the propagation when meeting an already selected edge
		Type            : bool
		
		PARAMETER       : Arc
		Brief           : Use an arc of the existing selection network as input
		Type            : table
		
		The arc is selected by the first ID in "IDs". When combined in delesection mode it can be used to re
		move arc of the existing selection network easily
		
		Remark: This mode has a meaning only if ##Deselect## is specified
		
		
		PARAMETER       : Parallel
		Brief           : Parallel edge selection algorithm
		Type            : bool
		
		Use the IDs list or extend the current edge selection set by selecting the parallel edges
		
		Remark: If ##Selected## is specified, the current selection will be used as input
		
		Remark: If ##Selected## is not specified, the specified in ##IDs## will be used as input
		
		
		PARAMETER       : Border
		Brief           : Select the borders of islands
		Type            : bool
		
		Remark: Avaible only when ##PrimType## == "Edge" or if ##PrimType## == "Vertex"
		
		
		PARAMETER       : Grow
		Brief           : Grow current selection
		Type            : bool
		
		Remark: Avaible only when ##PrimType## == "Edge" or if ##PrimType## == "Vertex" or if ##PrimType## =
		        = "Polygon"
		
		
		PARAMETER       : Shrink
		Brief           : Shrink current selection
		Type            : bool
		
		Remark: Avaible only when ##PrimType## == "Edge" or if ##PrimType## == "Vertex" or if ##PrimType## =
		        = "Polygon"
		
		
		PARAMETER       : Highlighted
		Brief           : Use the current highlighted primitive has input
		Type            : bool
		
		PARAMETER       : Raycast
		Brief           : Enable ray casting
		Type            : bool
		
		Remark: Currently used only for ##PyramidalFrustum##
		
		
		PARAMETER       : Element
		Brief           : Select or extend the current selection state of the current ##PrimType## to cover a full mesh element
		Type            : table
		
		Mesh element means a connected set of primitives of the 3D topology.
		
		If ##IDs## is specified, its content is used as a seed set. On the contrary, the selection state is 
		taken as seed set.
		
		
		PARAMETER       : PyramidalFrustum.Section
		Brief           : Select using a volume which is defined by a pyramidal frustum
		Type            : doubles
		
		##Section## is the base of the pyramid [x0 y0 z0 x1 y2 z3 ... xn-1 yn-1 zn-1]
		
		See http://mathworld.wolfram.com/PyramidalFrustum.html
		
		
		PARAMETER       : PyramidalFrustum.SectionNormal
		Brief           : Pyramid section's normal
		Type            : vector3d
		
		PARAMETER       : PyramidalFrustum.Height
		Brief           : Height of the pyramid from its base to its top
		Type            : double
		
		PARAMETER       : PyramidalFrustum.Apex
		Brief           : Pyramid apex coordinates
		Type            : vector3d
		
		Remark: If the apex is not specified, the defined volume will be simple extrusion of the section. 
		
		
		PARAMETER       : PyramidalFrustum.Crossing
		Brief           : For edge primitives, select those that go across the bounding pyramidal frustum volume
		Type            : bool
		
		PARAMETER       : SmoothingGroups
		Brief           : Use the smoothing groups as input for the operation
		Type            : ints
		
		PARAMETER       : PolyGroups
		Brief           : Use the polygroups as input for the operation
		Type            : strings
		
		PARAMETER       : Materials
		Brief           : Use the materials as input for the operation
		Type            : strings
		
		PARAMETER       : Objects
		Brief           : Use the objects name as input for the operation
		Type            : strings
		
		PARAMETER       : Convert
		Brief           : Use current selection state from a primitive type to another one
		Type            : table
		
		PARAMETER       : Convert.Source
		Brief           : Source primitive type
		Type            : string
		
		Remark: the destination primitive is implicitly defined by ##PrimType##
		
		
		PARAMETER       : Range
		Brief           : Select by value range of a specified characteristic
		Type            : table
		
		PARAMETER       : Range.Mode
		Brief           : Characteristic on which the selection will be determined
		Type            : string
		Possible Values :
		                 - Distortion
		                 - AbsoluteStretch
		                 - Size
		
		Remark: Size is the maximum size of the bounding box in UV space, is only available in island mode.
		
		
		PARAMETER       : Range.Min
		Brief           : Minimim value of the characteristic
		Type            : double
		
		PARAMETER       : Range.Max
		Brief           : Maximum value of the characteristic
		Type            : double
		
		PARAMETER       : Range.NAN
		Brief           : Include exclusivelly values that are not a number (excluding others values)
		Type            : bool
		
		PARAMETER       : Auto
		Brief           : Auto Selection Algorithms
		Type            : table
		
		PARAMETER       : Auto.Quality
		Brief           : Normalized Threshold [0...1] used to qualify the validity of the generated segmentation
		Type            : double
		
		Currently this parameter is only used when the "StretchLimiter" is activated (see below). If the qua
		lity obtained by an algorithm such as "Skeleton" or "Quasidevelopable" or "Box" etc... give a segmen
		tation that creates too much stretching after flattening, the ##Auto.StretchLimiter## algorithm will
		 update (add more cuts) to the segmentation in order to get a mesh more developable.
		
		
		PARAMETER       : Auto.Smooth
		Brief           : Pre-smooth the geometry. Can be used to filter noise that creates over segmentation
		Type            : table
		
		PARAMETER       : Auto.Smooth.Iterations
		Brief           : Smooth Iteration count (mandatory)
		Type            : int
		
		PARAMETER       : Auto.Smooth.Force
		Brief           : Smooth force (mix) value [0...1] (mandatory)
		Type            : double
		
		PARAMETER       : Auto.Smooth.MapName
		Brief           : If specified, the map name of the vertex map that will be used to control the influence of the smooth Force for each vertex (Force will be multiplied with the map's values)
		Type            : string
		
		PARAMETER       : Auto.Skeleton
		Brief           : AUTO SKELETON (named "HIERARCHICAL" in the standalone version)
		Type            : table
		
		Transform the mesh into a thin skeleton, then link all skeleton extremities with path of edges (edge
		 selection set). The skeleton joints can also be selected using ##Auto.Skeleton.SegLevels##
		
		
		PARAMETER       : Auto.Skeleton.Open
		Brief           : Select edges using shortest paths that links extremities of the skeleton
		Type            : bool
		
		PARAMETER       : Auto.Skeleton.SegLevels
		Brief           : Specify which levels of the skeleton should be selected. The skeleton joints will be cut depending of theirs position in the skeleton hierarchy level
		Type            : ints
		
		PARAMETER       : Auto.PipesCutter
		Brief           : AUTO PIPECUTTER (named "LINK HOLES" in the standalone version)
		Type            : bool
		
		Use this option to link all holes using path of edges
		
		
		PARAMETER       : Auto.HandleCutter
		Brief           : AUTO HANDLECUTTER (named "CUT HANDLES" in the standalone version)
		Type            : bool
		
		Use this option to suppress handles. This will reduce the genus of the mesh so that it will become d
		evelopable
		
		
		PARAMETER       : Auto.QuadLoopCutter
		Brief           : Extract regular grid loops
		Type            : bool
		
		Use this option to cut tube-like geometry and revolution shapes. Well suited for cylinders and extru
		ded shapes.
		
		
		PARAMETER       : Auto.QuasiDevelopable
		Brief           : AUTO QUASIDEVELOPABLE (named "MOSAIC" in the standalone version)
		Type            : table
		
		PARAMETER       : Auto.QuasiDevelopable.Developability
		Brief           : Developability threshold
		Type            : double
		
		Values near 0 will select nothing and the resulting cut network would likely be hard to by unwrapped
		. Values near 1 will select all curved parts resulting in a high number of new islands, easily unwra
		ppable with no few stretching
		
		Remark: Can be seen as the segmentation force
		
		
		PARAMETER       : Auto.QuasiDevelopable.IslandPolyNBMin
		Brief           : Minimum polygons count under which a given island can be segmented into new separate parts
		Type            : int
		
		PARAMETER       : Auto.QuasiDevelopable.AreaMinRatio
		Brief           : Minimum value allowed of the ratio newIslandArea / originalIslandArea
		Type            : double
		
		Values near 0 will allow the creation of many new small islands. Values near 1 will prevent the crea
		tion of small islands
		
		Remark: Enable it by specifying the parameter to the task
		
		
		PARAMETER       : Auto.QuasiDevelopable.FitCones
		Brief           : Try to fit cones and cylindrical shapes
		Type            : bool
		
		If false or not speficied, the algorithm will fit only planes, resulting in more islands
		
		Remark: This option make the computation time longer
		
		
		PARAMETER       : Auto.QuasiDevelopable.Straighten
		Brief           : Enable island border straightening 
		Type            : bool
		
		PARAMETER       : Auto.QuasiDevelopable.IslandsNB
		Brief           : Each island of the working set will be segmented into the specified number of parts
		Type            : int
		
		Remark: Enable it by specifying the parameter
		
		
		PARAMETER       : Auto.Box
		Brief           : Select edges like if each islands would have a geometry close to a box
		Type            : table
		
		PARAMETER       : Auto.Box.ActiveEdges
		Brief           : Select only the specified edges of the virtual box
		Type            : strings
		
		For instance, to select edges X+Y+ and X-Z+, the string vector should contains ["XPYP", "XMZP"]  
		
		
		PARAMETER       : Auto.SharpEdges.AngleMin
		Brief           : Select edges when the angle of the normals of the connected polygons is superior to the specified value
		Type            : double
		
		PARAMETER       : Auto.StretchLimiter
		Brief           : Improve the edge selection set to limit the resulting stretching
		Type            : table
		
		Will flatten a copy of the islands and measure the stretching an angular distortion. If the quality 
		is below a threshold, add more cuts to the segmentation
		
		Remark: WUse "Auto.FlatteningMode" to specify the flattening method used for the stretching check
		
		
		Brief           : Flattening Mode for Automatic Selection
		Type            : 
		Possible Values :
		                 - SELECT_AUTO_FLATTENING_MODE_UNFOLD
		                 - SELECT_AUTO_FLATTENING_MODE_AVERAGE_NORMAL
		                 - SELECT_AUTO_FLATTENING_MODE_BOX
		
		PARAMETER       : Auto.FlatteningMode
		Brief           : Flattening algorithm used for the ##Auto.StretchLimiter##, ##Auto.SkeletonUnoverlap## and ##Auto.BooleanUnoverlap##
		Type            : int
		
		Available mode are: (see enum ##SELECT_AUTO_FLATTENING_MODES##) 
		
		  - 0 for unfold method (best results) 
		
		  - 1 for average normal method (faster results)
		
		  - 2 when used with the ##Auto.Box## master tool (if you wish to have restrict your projections to 
		    Cube like)
		
		
		PARAMETER       : Auto.FlatteningUnfoldParams
		Brief           : Unfold parameters for flattening method unfold
		Type            : table
		
		If the flattening algorithm is 0 (unfold), the given parameters will be used when unfolding the alre
		ady segmented islands. Have look at task Unfold to see available parameters.
		
		
		PARAMETER       : Auto.StoreCoordsUVW
		Brief           : Store computed UV coordinates
		Type            : bool
		
		If enabled, the UVs coordinates computed during validity checks (see StretchLimiter) are stored in t
		he table "Mesh.Tmp.AutoSelect.UVWs" instead of being deleted after the computation. Theses UV coordi
		nates can then further be red and used in an Import task or to redefine the UVs of the host applicat
		ion.
		
		The created structure a table that contains:
		
		  - a vector of integers (ints) named "PolyVertIDs" containing the PolyVertIDs of the vertexes 
		
		  - a vector of doubles (doubles) named "UVWs" containing the folded UVW coordinates [u0 v0 w0 u1 v1
		     w1 u2 v2 w2 ... un-1 vn-1 wn-1]
		
		The vertex specified at position 2p in "PolyVertIDs" has the coordinates at position 3p, 3p+1, 3p+2 
		in the vector "UVWs" 
		
		Remark:  Using these UV coordinates allows to avoid to recompute the flattening/unfolding. It is rec
		        ommended to use them since they are guaranteed to be overlap free and invalid stretches free
		        , contrary to the one that could be generated after a cut and a new unfold (since the used p
		        arameters could be different).
		
		
		PARAMETER       : Auto.OutputCoordsUVW
		Brief           : Output computed UV coordinates
		Type            : bool
		
		If enabled, the UVs coordinates computed during validity checks (see StretchLimiter) will be outputt
		ed instead of being deleted. Theses UV coordinates can then further be red and used in an Import tas
		k or to redefine the UVs of the host application.
		
		The created structure a table that contains:
		
		  - a vector of integers (ints) named "PolyVertIDs" containing the PolyVertIDs of the vertexes 
		
		  - a vector of doubles (doubles) named "UVWs" containing the folded UVW coordinates [u0 v0 w0 u1 v1
		     w1 u2 v2 w2 ... un-1 vn-1 wn-1]
		
		The vertex specified at position 2p in "PolyVertIDs" has the coordinates at position 3p, 3p+1, 3p+2 
		in the vector "UVWs" 
		
		Remark:  Using these UV coordinates allows to avoid to recompute the flattening/unfolding. It is rec
		        ommended to use them since they are guaranteed to be overlap free and invalid stretches free
		        , contrary to the one that could be generated after a cut and a new unfold (since the used p
		        arameters could be different).
		
		
		PARAMETER       : Auto.SkeletonUnoverlap
		Brief           : Skeleton Unoverlap (post operation)
		Type            : table
		
		Virtually flatten islands using the generated segmentation and detect if there is presence of overla
		ps. If there is presence of overlaps the mesh will be segmented more in order to remove the overlaps
		
		
		PARAMETER       : Auto.BooleanUnoverlap
		Brief           : Boolean Unoverlap (post operation)
		Type            : table
		
		Virtually flatten islands using the generated segmentation and detect if there is presence of overla
		ps. If there is presence of overlaps the mesh will be segmented more in order to remove the overlaps
		
		
		PARAMETER       : Auto.SizeLimiter.LengthRatio
		Brief           : When present, size limiter will update the seams if island if it is too big
		Type            : double
		
		The admissible island length ratio. If the maximum bounding box length of a given island over the av
		erage of the maximum bb length exceeds the LengthRatio, the island will be cut in two.
		
		
		PARAMETER       : Auto.ReWeld
		Brief           : Auto reweld (almost final post operation)
		Type            : table
		
		ReWeld lower the selected edges count if possible by virtually try to stitch islands without creatin
		g overlaps. It is useful when the cut line given by AUTO selection gives too much small islands or w
		hen dealing with hard surface model that have been to much cut on their sharp angles.
		
		Remark: ReWeld work only on the edge selected in the same task instance, not with the existing cuts.
		
		
		PARAMETER       : Auto.ReWeld.Threshold
		Brief           : Auto reweld threshold
		Type            : double
		
		Maximum relative distance between two edges that allows them to be welded. The distance is relative 
		to the average edge length.
		
		
		PARAMETER       : Auto.ReWeld.PolyMax
		Brief           : Auto reweld maximum polygon count
		Type            : int
		
		Authorize welding of a given island if its polycount is below the specified value
		
		
		PARAMETER       : Auto.ReWeld.LenghtMax
		Brief           : Auto reweld maximum lenght
		Type            : double
		
		Authorize welding of an island if its bounding box maximum lenght is below the specified value 
		
		
		OUTPUT      : Auto.UVW
		Brief           : Outputed computed UV coordinates
		Type            : table
		
		if ##Auto.OutputCoordsUVW## bool parameter is present and true, the variable will contain the UVs co
		ordinates computed during validity checks (see ##Auto.StretchLimiter##) 
		
		The created structure a table that contains:
		
		  - a vector of integers (ints) named "PolyVertIDs" containing the PolyVertIDs of the vertexes 
		
		  - a vector of doubles (doubles) named "UVWs" containing the UVW coordinates [u0 v0 w0 u1 v1 w1 u2 
		    v2 w2 ... un-1 vn-1 wn-1]
		
		The vertex specified at position 2p in "PolyVertIDs" has the coordinates at position 3p, 3p+1, 3p+2 
		in the vector "UVWs" 
		
		Remark:  Using these UV coordinates allows to avoid to recompute the flattening/unfolding. It is rec
		        ommended to use them since they are guaranteed to be overlap free and invalid stretches free
		        , contrary to the one that could be generated after a cut and a new unfold (since the used p
		        arameters could be different).
		
		
		
		"""
		return self.rizomuv.Execute('Select', p)

	def Move(self, p):
		"""
		Manage UVSet
		
		PARAMETER       : PrimType
		Brief           : Processed primitive type
		Type            : string
		Possible Values :
		                 - "Vertex"
		                 - "Edge"
		                 - "Triangle"
		                 - "Island"
		
		PARAMETER       : WorkingSet
		Brief           : The island set on which the task will be applied
		Type            : string
		Default         : "Visible&UnLocked"
		Possible Values :
		                 - "Visible"
		                 - "Selected"
		                 - "Flat"
		                 - "NotFlat"
		
		Remark: Combinations are possible like "Visible&Selected&Flat"
		
		
		PARAMETER       : Transform
		Brief           : Transformation matrix used to transform the processed elements
		Type            : matrix3d
		
		PARAMETER       : CenterMode
		Brief           : Transformation center mode
		Type            : string
		Possible Values :
		                 - "Matrix"        : (default), no re-centering is done. (The transformation matrix itself contains the necessary)
		                 - "COG"        : Center of gravity, computed using all selected elements
		                 - "MultiCOG"        : Multi center of gravity. The selection is segmented into connected elements set. Each of them get his own center of gravity.
		                 - "BBox"        : Center of bounding box, computed using all selected elements
		                 - "MultiBBox"        : Multi center of bounding boxes. The selection is segmented into connected elements set. Each of them get his own center of bounding box.
		
		PARAMETER       : Geometrical
		Brief           : Selects one of the miscellaneous algorithms that moves and deforms the UVs coordinates
		Type            : string
		
		Remark: See task deform and parameter Geometrical to see possible values
		
		
		
		"""
		return self.rizomuv.Execute('Move', p)

	def Deform(self, p):
		"""
		Deform or transform the selected uv coordinates using specified algorithms
		
		This task has 3 main modes
		
		  1. ##BrushStroke## : The coordinates are transformed using a list of "brushes"
		
		  2. ##Geometrical## : Misc algorithms such as Align / Rectangularize / SnapToGrid etc...
		
		  3. ##Transform## : The coordinates are transformed using a transformation matrix
		
		Remark: Optimize iterations can be applied in post process if ##Optimize## parameter table is specif
		        ied (see "Optimize" task parameter definition in that document)
		
		PARAMETER       : WorkingSet
		Brief           : The island set on which the task will be applied
		Type            : string
		Default         : "Visible&UnLocked"
		Possible Values :
		                 - "Visible"
		                 - "Selected"
		                 - "Flat"
		                 - "NotFlat"
		
		Remark: Combinations are possible like "Visible&Selected&Flat"
		
		
		PARAMETER       : PrimType
		Brief           : The primitive type that will be processed
		Type            : string
		Default         : "Edge"
		Possible Values :
		                 - "Vertex"
		                 - "Edge"
		                 - "Triangle"
		                 - "Polygon"
		                 - "Island"
		
		PARAMETER       : CenterMode
		Brief           : Transformation center mode
		Type            : string
		Possible Values :
		                 - "Matrix"        : (default), no re-centering is done. (The transformation matrix itself contains the necessary)
		                 - "COG"        : Center of gravity, computed using all selected elements
		                 - "MultiCOG"        : Multi center of gravity. The selection is segmented into connected elements set. Each of them get his own center of gravity.
		                 - "BBox"        : Center of bounding box, computed using all selected elements
		                 - "MultiBBox"        : Multi center of bounding boxes. The selection is segmented into connected elements set. Each of them get his own center of bounding box.
		
		Remark: This parameters has an influence only for modes ##Transform## and ##Geometrical## with most 
		        of its sub modes. In case of main mode ##Geometrical##, "Matrix" and "COG" are equivalent
		
		
		PARAMETER       : UseSelectionMask
		Brief           : Use small primitives (vertexes/edges/triangles/polygons) selection state as positive mask
		Type            : bool
		
		Remark: Has influence only for ##BrushStroke## main mode
		
		Remark: To process only selected islands use the appropriate value of ##WorkingSet##
		
		
		PARAMETER       : PinMapName
		Brief           : Pin map name
		Type            : string
		
		Vertexes that have pin values > 0 will tend to stay at their current position.
		
		Remark: Works only for main modes ##Transform## and ##BrushStroke##
		
		
		PARAMETER       : Transform
		Brief           : Transformation matrix used to transform the processed elements in the UV space
		Type            : matrix3d
		
		This should be a 3x3 matrix for 2 dimensionnal affine transformations, which would transform P into 
		T*P, where the 2 first values of column vector P are the u and v coordinates. The last column contai
		n the translation vector.
		
		
		Remark: Falloff can be applied (see ##Proportional.FallOffDistance## and ##Proportional.FallOffProfi
		        leType##)
		
		
		PARAMETER       : ProjectionMatrix
		Brief           : Transformation matrix used to project the processed elements of the 3D space into the UVW space
		Type            : matrix3d
		
		This should be a 3x3 matrix for 3 dimensionnal transformations, which transform a 3D position x,y,z 
		into u,v,w.
		
		
		Remark: To project in the UV space only (the w = 0 plane), the last line of the matrix must be zeros
		        .
		
		
		PARAMETER       : ResetIslandScale
		Brief           : Reset the island scale before appliyng the transformation
		Type            : bool
		
		Each processed islands will be rescaled so that they get their original 3D area before being transfo
		rmed
		
		Remark: This will be taken into account only if ##Transform## is specified and ##PrimType## == "Isla
		        nd"
		
		
		PARAMETER       : IDs
		Brief           : The primitive IDS that will be processed
		Type            : ints
		
		Currently only Island IDs can be specified, other primitives type must be selected by a selection ta
		sk before
		
		Remark: Falloff can be applied (see ##Proportional.FallOffDistance## and ##Proportional.FallOffProfi
		        leType##)
		
		
		PARAMETER       : Proportional.FallOffDistance
		Brief           : Activate the proportional transformation
		Type            : double
		
		Remark: Only available with the ##Transform## main mode
		
		This value defines the transformation falloff distance from the selection set. If this parameter is 
		specified, ##Proportional.FallOffProfileType## must be specified as well.
		
		
		PARAMETER       : Proportional.FallOffProfileType
		Brief           : Falloff profile type
		Type            : int
		Possible Values :
		                 - 0        : Constant   : 1.0
		                 - 1        : Linear     : 1.0-x/r
		                 - 2        : Sharp      : (1.0-x/r) * (1.0-x/r)
		                 - 3        : Root       : 1.0-(x*x/(r*r))
		                 - 4        : Sphere     : sqrt(fabs(1.0-(x*x/(r*r))))
		                 - 5        : Smooth     : exp(-4 * x * x / (r*r)) -exp(-4.)*x/r
		
		Where r is the falloff distance
		
		Remark: Currently this parameter influences only when ##Transform## main mode is specified
		
		
		PARAMETER       : BrushStroke
		Brief           : Brush stroke
		Type            : table
		
		Contains a list of brush structures. Each brush structure represent a touch of a pencil and contains
		 a transformation matrix, a mix value and a falloff profile
		
		Remark: Brush data structure are exposed as D_BRUSH_X in that document. All brush touches must be sp
		        ecified in a table
		
		
		PARAMETER       : Geometrical
		Brief           : Selects one of the miscellaneous algorithms that moves and deforms the UVs coordinates
		Type            : string
		Possible Values :
		                 - "PlanarProjection"        : Project the selection set among the island working set on the plane defined by first row of the 3d matrix specified by ##ProjectionMatrix##
		                 - "ProjectBox"        : Project selection on the faces of a virtual box. The average normal of each connected polygon groups determines on which faces the polygons will be 
		                 - "ProjectAvgNormal"        : Use the selection to define an average normal then project the selection to the associated orthogonal plane then finally rotate the result in order to be placed in the UV plane
		                 - "FitToGridLarger"        : Fit selected elements to the grid by enlarging them. The grid must be specified using using ##GridSize## and ##GridOffset##.
		                 - "FitToGridSmaller"        : Fit selected elements to the grid by reducing them. The grid must be specified using using ##GridSize## and ##GridOffset##.
		                 - "FitToGridClosest"        : Fit selected elements to the grid by enlarging or reducing them. The grid must be specified using using ##GridSize## and ##GridOffset##.
		                 - "AlignRight"        : Move selected elements so that their bounding boxes are aligned on their right
		                 - "AlignLeft"        : Move selected elements so that their bounding boxes are aligned on their left
		                 - "AlignTop"        : Move selected elements so that their bounding boxes are aligned on their top
		                 - "AlignBottom"        : Move selected elements so that their bounding boxes are aligned on their right
		                 - "AlignHorizontal"        : Move selected elements so that their bounding boxes are aligned horizontally
		                 - "AlignVertical"        : Move selected elements so that their bounding boxes are aligned vertically
		                 - "CrushRight"        : Crush selected elements so that their bounding boxes are aligned on their right
		                 - "CrushLeft"        : Crush selected elements so that their bounding boxes are aligned on their left
		                 - "CrushTop"        : Crush selected elements so that their bounding boxes are aligned on their top
		                 - "CrushBottom"        : Crush selected elements so that their bounding boxes are aligned on their right
		                 - "CrushHorizontal"        : Crush selected elements so that their bounding boxes are aligned horizontally
		                 - "CrushVertical"        : Crush selected elements so that their bounding boxes are aligned vertically
		                 - "FlipHorizontal"        : Mirror selected elements using the Y axis which is centered on the selected element's bounding box. The flipping axis position can also be defined using ##AxisPosition##.
		                 - "FlipVertical"        : Mirror selected elements using the X axis which is centered on the selected element's bounding box. The flipping axis position can also be defined using ##AxisPosition##
		                 - "FlipHorizontalLeft"        : Mirror selected elements using a Y axis located on the bounding box's left side of the selected elements. The flipping axis position can also be defined using ##AxisPosition##
		                 - "FlipVerticalTop"        : Mirror selected elements using a X axis located on the bounding box's top side of the selected elements. The flipping axis position can also be defined using ##AxisPosition##
		                 - "FlipHorizontalRight"        : Mirror selected elements using a Y axis located on the bounding box's right side of the selected elements. The flipping axis position can also be defined using ##AxisPosition##
		                 - "FlipVerticalBottom"        : Mirror selected elements using a X axis located on the bounding box's bottom side of the selected elements. The flipping axis position can also be defined using ##AxisPosition##
		                 - "StackSymmetricalMaster"        : Fold symmetric islands over their counterparts: Remark: The symmetry must be activated. The master elements will not move.
		                 - "StackSymmetricalSlave"        : Fold symmetric islands over their counterparts: Remark: The symmetry must be activated. The slave elements will not moved.
		                 - "Align"        : If applied on edges, the selected vertexes will be aligned. If applied on edges, the selected edges will be aligned, each of group of connected edges will aligned independently
		                 - "Parallelize"        : Make the selection parallel. If applied on quads, each group of connected quads will form a regular grid. If applied on islands, the island should be composed of quads only. If applied on edges, each group of connected edges will become horizontal
		                 - "Verticalize"        : Make the selection vertical. If applied on quads, each group of connected quads will form a regular grid aligned on the Y axis. If applied on islands, the island should be composed of quads only. If applied on edges, each group of connected edges will become horizontal
		                 - "Horizontalize"        : Make the selection horizontal. If applied on quads, each group of connected quads will form a regular grid aligned on the X axis. If applied on islands, the island should be composed of quads only. If applied on edges, each group of connected edges will become horizontal
		                 - "TransformIslandsByEdgePairs"        : Can be applied on border edges only. Transform the opposite island connected to a border edge so that it stitches to the selected border edge
		                 - "AlignIslandToSelection"        : Rotate islands so that they align to the selected elements of the specified primitive type (border edges or border polygon)
		                 - "DistributeSpaceHorizontally"        : Distribute the available space between selected items horizontally
		                 - "DistributeSpaceVertically"        : Distribute the available space between selected items vertivally
		                 - "DistributeLeft"        : Distribute the objects so that all left bounding boxes side will be equaly distant from each others
		                 - "DistributeCenterHorizontally"        : Distribute the objects so that all center bounding boxes side will be equaly distant from each others
		                 - "DistributeRight"        : Distribute the objects so that all right bounding boxes side will be equaly distant from each others
		                 - "DistributeBottom"        : Distribute the objects so that all left bounding boxes side will be equaly distant from each others
		                 - "DistributeCenterVertically"        : Distribute the objects so that all center bounding boxes side will be equaly distant from each others
		                 - "DistributeTop"        : Distribute the objects so that all right bounding boxes side will be equaly distant from each others
		
		PARAMETER       : IntervalSize
		Brief           : Interval size in real unit for distribute sub modes
		Type            : double
		
		Remark: Used when ##Geometrical## is equal to "DistributeSpaceHorizontally" or "DistributeSpaceVerti
		        cally" sub modes
		
		
		PARAMETER       : GridSize
		Brief           : Grid reference element U, V and Wdimensions
		Type            : vector3d
		
		Remark: Currently used along with ##Geometrical## main mode and its "SnapToGrid", "FitToGridLarger",
		         "FitToGridSmaller" and "FitToGridClosest" sub modes
		
		Remark: The Z coordinate is currently ignored
		
		
		PARAMETER       : GridOffset
		Brief           : Grid reference element offset
		Type            : vector3d
		
		If not specified, the default value will be the origin (0,0,0)
		
		Remark: Currently used along with ##Geometrical## main mode and its "SnapToGrid", "FitToGridLarger",
		         "FitToGridSmaller" and "FitToGridClosest" sub modes
		
		Remark: W is currently unused
		
		
		PARAMETER       : AxisPosition
		Brief           : Axis position of the flipping axis
		Type            : double
		
		Remark: Currently used for ##Geometrical## main mode and its "FlipHorizontal" and "FlipVertical" sub
		         modes
		
		
		PARAMETER       : Rotation
		Brief           : Rotation
		Type            : double
		
		Remark: It is not used in ##Transform## mode
		
		
		PARAMETER       : Optimize
		Brief           : Optimize parameters
		Type            : table
		
		Optimize iterations can be added as a post process to reduce stretching caused by the deformation.
		
		Remark: Combination of Optimize and ##Transform## mode allows deformation to be done in real-time us
		        ing the Update feature of the API
		
		
		PARAMETER       : ElasticMode
		Brief           : Rotation
		Type            : bool
		
		If enabled, the selection will behave like rubber, else it will behave like a modeling clay.
		
		
		PARAMETER       : ApplyOptimizeOnUpdate
		Brief           : Enable Optimize on update only mode
		Type            : bool
		
		If enabled, the optimize algorithm will be applied only when calling CRizomUVAPI::Update() and not C
		RizomUVAPI::Execute
		
		Remark: This will have an influence only if ##Optimize## is specified
		
		
		PARAMETER       : ProcessSelection
		Brief           : Process all if the selection corresponding to ##PrimType## is empty
		Type            : bool
		
		
		"""
		return self.rizomuv.Execute('Deform', p)

	def IslandProperties(self, p):
		"""
		Define some of the islands properties
		
		PARAMETER       : IslandIDs
		Brief           : Island IDs of islands that properties will be added/modified
		Type            : ints
		
		PARAMETER       : IslandByPolygonIDs
		Brief           : Polygon IDs that will be used to define the set of islands that will have their properties be added/modified			 
		Type            : ints
		
		PARAMETER       : Properties
		Brief           : Properties inside the island root that will be added / modified
		Type            : table (PackElemProperties)
		
		Remark: Adding the constraints doesn't move any UV vertexes. If you want to update the flattened geo
		        metry according to  new constraints, you have to execute an Unfold or Optimize task
		
		
		PARAMETER       : MergingPolicy
		Brief           : Policy while merging the properties tree
		Type            : int
		
		Remark: Prefer using the string version ##MergingPolicyString##.
		
		The default value is additive mode: "A_ADD|AIB_ADD_A_VALUE_B|B_CLONE". New values replace the old on
		es if their path match. Old unmatched variables are kept
		
		
		PARAMETER       : MergingPolicyString
		Brief           : Policy while merging the properties tree in string version
		Type            : string
		Possible Values :
		                 - A_IGNORE        : Ignore element
		                 - A_ADD        : Add element
		                 - A_THROW        : Generate an error
		                 - A_CLONE        : Clone the element
		                 - B_IGNORE        : Ignore element
		                 - B_ADD        : Add element
		                 - B_THROW        : Generate an error
		                 - B_CLONE        : Clone the element
		                 - AIB_IGNORE        : Ignore both elements 
		                 - AIB_ADD_A        : Add element A. Elem A must be convertible to elem B's type 
		                 - AIB_ADD_B        : Add element B. Elem B must be convertible to elem A's type
		                 - AIB_CLONE_A        : Clone element A. Elem A must be convertible to elem B's type
		                 - AIB_CLONE_B        : Clone element B. Elem B must be convertible to elem A's type
		                 - AIB_ADD_A_VALUE_B        : Add the type of A using B's value. Elem A must be convertible to elem B's type (add A but use the value of B) this is useful when A has a derived class of CVal. After merging A will keep is derived data. 
		                 - AIB_ADD_B_VALUE_A        : Add the type of B using A's value. elem B must be convertible to elem A (add B but use the value of A) this is useful when B has a derived class of CVal. After merging B will keep is derived data. 
		                 - AIB_FORBID_CONVERSION        : If the type are not equal exactly then throw
		                 - AIB_IGNORE_INVALID_A        : If elem in A is invalid it will be not added to the merged table (useful for removing elements from table B using a invalid CRefs in table A as a deleting mask)
		                 - AIB_IGNORE_INVALID_B        : If elem in B is invalid it will be not added to the merged table (useful for removing elements from table A using a invalid CRef in table B as a deleting mask)
		                 - AIB_IGNORE_LEAF_A        : If elem in A is not a table it will be not added to the merged table (useful for removing elements from table B using a dummy element in table A)
		                 - AIB_IGNORE_LEAF_B        : If elem in B is not a table it will be not added to the merged table (useful for removing elements from table A using a dummy element in table B) 
		
		When merging the internal data structure A with the given one B, the two trees are merged to form th
		e new internal data structure. This parameter specifies how this merging should be done.
		
		The default value is additive mode: "A_ADD|AIB_ADD_A_VALUE_B|B_CLONE". New values replace the old on
		es if their path match. Old unmatched variables are kept
		
		
		
		"""
		return self.rizomuv.Execute('IslandProperties', p)

	def IslandGroups(self, p):
		"""
		Manage the island group hierarchy
		
		A group is a container of island indexes and groups (children group). A Tile is a group that have sp
		ecial properties and it is considered differently in many aspects, notably in the packing task where
		 the tiles are never scaled rotated transformed, contrary to regular groups
		
		Example of a typical group hierarchy containing two tiles, tree regular groups and some islands ID d
		istributed over the groups:
		
		        	  RootGroup
		        			  |___Tile0
		        			  |       |__[0 5 2] (islandIDs)
		        			  |
		        			  |___Tile1
		        					  |__[1 6 7]
		        					  |
		        					  |__G0
		        						  |___[8 9 10 4]
		        						  |
		        						  |___G1
		        						  |    |__[3 11 12 13]
		        						  |
		        						  |___G2
		        							   |__[14 15 16]
		        			
		
		Remark: The SDK creates the built-in "RootGroup" inside the DAG mesh's root at mesh load. By default
		         the RootGroup contains a single tile.
		
		Remark: All groups contained in a given hierarchy (e.g "RootGroup") must not overlaps (an island can
		         only be referenced inside one group at a time). If some groups overlaps, algorithms such as
		         packing may produce unpredictable results.
		
		Remark: When a new group is created and added to the "RootGroup" hierarchy, the specified islands ID
		        s will be transfered from their current group the newly created group
		
		PARAMETER       : Mode
		Brief           : Define the operation applied on the group hierarchy
		Type            : string
		Default         : "DefineGroup"
		Possible Values :
		                 - "DefineGroup"        : Redefine (Create if needed) the group using ##GroupPath## and the set of island defined by ##IslandIDs## or ##IslandByPolygonIDs##. The islands are removed from their current group wherever they are in the group hierarchy to the group specified ##GroupPath##. If some groups are specified using ##IslandIDs## or ##IslandByPolygonIDs##, they will be also transfered to their current location to the group specified by ##GroupPath##. If ##NewName## is specified instead of ##GroupPath##, a new group will be created and placed into the container of the lowest element found in the element set composed by ##IslandIDs## or ##IslandByPolygonIDs## and ##GroupPath##. If the ##Properties## parameter is present the properties will be added to the group using the provided merging policy specified by ##MergingPolicy##.
					
		                 - "DistributeInGroupsByBBox"        : Insert the elemnts (the islands specified by ##IslandIDs##/##IslandByPolygonIDs## and the groups specified by ##GroupPaths##) into the existing groups. The bounding box center position of each element determine to which existing group the element will be inserted into. If the element center is included into several groups, the one with the higher level in the hierarchy will be used. The islands are removed from their current group wherever they are in the group hierarchy to their associated groups. Note that the element can be inserted into tiles too.
					
		                 - "Rename"        : Rename the group defined by ##GroupPath## using ##NewName##
		                 - "TransferToParent"        : Move the given islands IDs specified by the ##IslandIDs## or ##IslandByPolygonIDs## from their respective group to their respective parent group. The top island group of the hierarchy from which the operation will begin its recursion must be specified using ##GroupPath##, if not specified the operation is done o n the full hierarchy starting from the root group named "RootGroup". If some groups are specified using ##GroupPaths##, their content (island IDs and children groups) will be moved to their parent group. If the destination group is a rootgroup, the elements will be moved on the left of the UDim Grid.
		                 - "DistributeTilesContent"        : Distribute the content (islands and groups) of the active tiles to the group(s) specified by ##GroupPaths##. If ##GroupPaths## is not specfied, the destination group will be the "RootGroup".
		                 - "SetGroupProperties"        : Define properties of the specified group. The groups on which the operation is applied must be specified using ##GroupPaths##. Default is {"RootGroup"}
		                 - "SetMultiTileLayout"        : Define the multi tile layout of the RootGroup. Use ##TileRows## and ##TileColumns## to specify the tile layout geometry. The necessary tiles will be created in the Children table of the group GroupPath. Their name will follow the pattern Tile_[colID]_[rowID] with indexes colID and rowID starting from 0.
		                 - "DistributeInTilesEvenly        : Distribute all islands (and regular groups) into the tiles. The island assignation use an algorithm that distribute the elements evenly into the available tiles
		                 - "DistributeInTilesByBBox"        : Distribute all islands (and regular groups) into the tiles. The island assignation use their bounding box's center. Islands are assigned into the tile in which their bounding box center is located.
		
		PARAMETER       : WorkingSet
		Brief           : The island set on which the task will be applied
		Type            : string
		Default         : "Visible"
		Possible Values :
		                 - "Visible"
		                 - "Selected"
		                 - "Flat"
		                 - "NotFlat"
		
		Remark: Combinations are possible like "Visible&Selected&Flat"
		
		
		PARAMETER       : IslandIDs
		Brief           : Island IDs of islands that properties will be added/modified
		Type            : ints
		
		PARAMETER       : AutoDelete
		Brief           : Delete empty groups
		Type            : bool
		
		PARAMETER       : IslandByPolygonIDs
		Brief           : Polygon IDs that will be used to define the set of islands IDs involved
		Type            : ints
		
		Host applications may use this method to define the groups since they don't have the knowledge of th
		e islands definitions
		
		
		PARAMETER       : NewName
		Brief           : New base name used to rename the processed islands when ##Mode## = "Rename"
		Type            : string
		
		PARAMETER       : GroupPath
		Brief           : Group path of the child of "RootGroup" (or a group path if it is a grandchild of "RootGroup")
		Type            : string
		
		  - In case of group inserted inside the RootGroup use "RootGroup.Children.NewGroupName". Notice the
		     presence of "RootGroup" and the member "Children" inside the path
		
		  - In case of group inserted inside a group contained inside an other group "RootGroup.Children.Par
		    entGroupName.Children.NewGroupName"
		
		
		
		PARAMETER       : GroupPaths
		Brief           : Group pathS of the children of "RootGroup" (or group paths if it is grandchildren of "RootGroup")
		Type            : strings
		
		  - In case of group inserted inside the RootGroup use "RootGroup.Children.NewGroupName". Notice the
		     presence of "RootGroup" and the member "Children" inside the path
		
		  - In case of group inserted inside a group contained inside an other group "RootGroup.Children.Par
		    entGroupName.Children.NewGroupName"
		
		
		
		PARAMETER       : UseTileSelection
		Brief           : Use tile selection
		Type            : bool
		
		Used only if ##Mode## is equal to "DistributeInTilesEvenly" or "DistributeInTilesByBBox". When activ
		e, tile selection will be taken into account to determine the active set of tiles in which the islan
		ds and groups can be distributed
		
		
		PARAMETER       : UseTileLocks
		Brief           : Use tile locking states
		Type            : bool
		
		Used only if ##Mode## is equal to "DistributeInTilesEvenly" or "DistributeInTilesByBBox". When activ
		e, tile locking states will be taken into account to determine the active set of tiles in which the 
		islands and groups cannot be distributed
		
		
		PARAMETER       : UseIslandLocks
		Brief           : Use island locking states
		Type            : bool
		
		Used only if ##Mode## is equal to "DistributeInTilesEvenly" or "DistributeInTilesByBBox". When activ
		e, tile island locking state will be taken into account to determine the set of island that cannot b
		e distributed
		
		
		PARAMETER       : Properties
		Brief           : Properties inside the island root that will be added / modified
		Type            : table
		
		PARAMETER       : MergingPolicy
		Brief           : Policy while merging properties
		Type            : int
		
		Remark: Prefer using the string version ##MergingPolicyString##.
		
		The default value is additive mode: "A_ADD|AIB_ADD_A_VALUE_B|B_CLONE". New values replace the old on
		es if their path match. Old unmatched variables are kept
		
		
		PARAMETER       : MergingPolicyString
		Brief           : Policy while merging the properties tree in string version
		Type            : string
		Possible Values :
		                 - A_IGNORE        : Ignore element
		                 - A_ADD        : Add element
		                 - A_THROW        : Generate an error
		                 - A_CLONE        : Clone the element
		                 - B_IGNORE        : Ignore element
		                 - B_ADD        : Add element
		                 - B_THROW        : Generate an error
		                 - B_CLONE        : Clone the element
		                 - AIB_IGNORE        : Ignore both elements 
		                 - AIB_ADD_A        : Add element A. Elem A must be convertible to elem B's type 
		                 - AIB_ADD_B        : Add element B. Elem B must be convertible to elem A's type
		                 - AIB_CLONE_A        : Clone element A. Elem A must be convertible to elem B's type
		                 - AIB_CLONE_B        : Clone element B. Elem B must be convertible to elem A's type
		                 - AIB_ADD_A_VALUE_B        : Add the type of A using B's value. Elem A must be convertible to elem B's type (add A but use the value of B) this is useful when A has a derived class of CVal. After merging A will keep is derived data. 
		                 - AIB_ADD_B_VALUE_A        : Add the type of B using A's value. elem B must be convertible to elem A (add B but use the value of A) this is useful when B has a derived class of CVal. After merging B will keep is derived data. 
		                 - AIB_FORBID_CONVERSION        : If the type are not equal exactly then throw
		                 - AIB_IGNORE_INVALID_A        : If elem in A is invalid it will be not added to the merged table (useful for removing elements from table B using a invalid CRef in table A as a deleting mask)
		                 - AIB_IGNORE_INVALID_B        : If elem in B is invalid it will be not added to the merged table (useful for removing elements from table A using a invalid CRef in table B as a deleting mask)
		                 - AIB_IGNORE_LEAF_A        : If elem in A is not a table it will be not added to the merged table (useful for removing elements from table B using a dummy element in table A)
		                 - AIB_IGNORE_LEAF_B        : If elem in B is not a table it will be not added to the merged table (useful for removing elements from table A using a dummy element in table B) 
		
		When merging the internal data structure A with the given one B, the two trees are merged to form th
		e new internal data structure. This parameter specifies how this merging should be done.
		
		The default value is additive mode: "A_ADD|AIB_ADD_A_VALUE_B|B_CLONE". New values replace the old on
		es if their path match. Old unmatched variables are kept
		
		
		PARAMETER       : Deselect
		Brief           : Deselect the group for ##Mode## == "SetGroupProperties" mode
		Type            : bool
		
		PARAMETER       : TileRows
		Brief           : Number of tile rows for ##Mode## == "SetMultiTileLayout"
		Type            : int
		
		PARAMETER       : TileColumns
		Brief           : Number of tile columns for ##Mode## == "SetMultiTileLayout"
		Type            : int
		
		PARAMETER       : UseIslandSelection
		Brief           : use island selection to determine the active set of islands
		Type            : bool
		
		PARAMETER       : FreezeIslands
		Brief           : Do not move islands coordinates while associating them into their destination tile
		Type            : bool
		
		PARAMETER       : IDsTransfer
		Brief           : Tranfers island IDs
		Type            : bool
		
		At the definition of a new group, the islands IDs of the new group will be transfered from their cur
		rent group to the new group. At the deletion of a group, the islands of the group will be transfered
		 to the parent group
		
		
		
		"""
		return self.rizomuv.Execute('IslandGroups', p)

	def Set(self, p):
		"""
		Set Application Variable Value
		"""
		return self.rizomuv.Execute('Set', p)

	def GenerateScriptingHelp(self, p):
		"""
		Generate Help String or File
		"""
		return self.rizomuv.Execute('GenerateScriptingHelp', p)

	def Quit(self, p):
		"""
		Quit this program with error code 0
		"""
		return self.rizomuv.Execute('Quit', p)

	def Exit(self, p):
		"""
		Exit the program with the given error code as argument
		"""
		return self.rizomuv.Execute('Exit', p)

	def SavePreferences(self, p):
		"""
		Save preferences and current settings
		"""
		return self.rizomuv.Execute('SavePreferences', p)

	def GenerateCheckerboardTexture(self, p):
		"""
		Generate the check board texture. Must be called if its resolution or repetition count changed.
		"""
		return self.rizomuv.Execute('GenerateCheckerboardTexture', p)

	def LoadUserTexture(self, p):
		"""
		Load a texture from an image file (used for the viewports in texture mode User)
		"""
		return self.rizomuv.Execute('LoadUserTexture', p)

	def LoadGridTexture(self, p):
		"""
		Load a texture from an image file (used for the viewports in texture mode Grid)
		"""
		return self.rizomuv.Execute('LoadGridTexture', p)

	def Count(self, p):
		"""
		Get table element count.
		"""
		return self.rizomuv.Execute('Count', p)

	def ItemNames(self, p):
		"""
		Get a list of the names of the items contained in the table.
		"""
		return self.rizomuv.Execute('ItemNames', p)

	def Eval(self, p):
		"""
		Evaluate function.
		"""
		return self.rizomuv.Execute('Eval', p)

	def Get(self, p):
		"""
		Get some application data.
		"""
		return self.rizomuv.Execute('Get', p)

	def GetAsString(self, p):
		"""
		Get some application data and transform them into a string.
		"""
		return self.rizomuv.Execute('GetAsString', p)

	def Test(self, p):
		"""
		Test internal code of RizomUV
		"""
		return self.rizomuv.Execute('Test', p)

	def LoadPrefs(self, p):
		"""
		Load preferences and set UI widgets according to the loaded values
		"""
		return self.rizomuv.Execute('LoadPrefs', p)

	def IslandCopy(self, p):
		"""
		Copy or select edge or island that have a similar topology
		
		Remark: Some UV vertexes are duplicated in UV space, so the UV topology is changed
		
		PARAMETER       : WorkingSet
		Brief           : The island set on which the task will be applied
		Type            : string
		Default         : "Visible&UnLocked"
		Possible Values :
		                 - "Visible"
		                 - "Selected"
		                 - "Flat"
		                 - "NotFlat"
		
		Remark: Combinations are possible like "Visible&Selected&Flat"
		
		
		PARAMETER       : Mode
		Brief           : 
		Type            : string
		Default         : "All"
		Possible Values :
		                 - "Selection"        : Copy the primitive selection state across all similar islands, or the select similar islands if ##PrimType## == "Island". The source islands are the ones that have at least one primitive selected among the set defined by ##WorkingSet##. The destination set is defined by ##WorkingSet##. If ##PrimType## == "Island" and if ##ReferenceIslandIDs## are both specified, the source island set is the one defined by ##ReferenceIslandIDs##.
		                 - "Stack"        : Copy the coordinates of the Source islands located in ##ReferenceIslandIDs## if specified or the ones defined by ##WorkingSet##
		                 - "Update"        : Update the coordinates of the Source islands located in ##ReferenceIslandIDs## if specified or the ones defined by ##WorkingSet##
		                 - "EdgesToCut"        : Return the edge IDs that could be used to cut the mesh so that the topology will be equal between the source islands and the matched ones. Source islands are ##ReferenceIslandIDs## if present or the ones defined by ##WorkingSet##
		                 - "EdgesToWeld"        : Return the edge IDs that could be used to weld the mesh so that the topology will be equal between the source islands and the matched ones. Source islands are ##ReferenceIslandIDs## if present or the ones defined by ##WorkingSet##
		
		PARAMETER       : PrimType
		Brief           : The primitive type used to determine the processed set
		Type            : string
		Possible Values :
		                 - "Vertex"
		                 - "Edge"
		                 - "Polygon"
		                 - "Island"
		
		Only used for 
		
		
		PARAMETER       : ReferenceIslandIDs
		Brief           : List of island indexes
		Type            : ints
		
		If ##Mode## == "Selection", this will work only with ##PrimType## == "Island"
		
		Reference / sources island IDs that will be used as reference for each stack
		
		The island working set must be specified using ##WorkingSet##
		
		
		PARAMETER       : AreaThreshold
		Brief           : Area threshold
		Type            : double
		
		When specified, if
		
		        |As-Ad|/max(As,Ad) > ##AreaThreshold##
		
		then the island will not be processed
		
		         Where As = sqrt(island source 3D space area) and Ad = sqrt(island destination 3D space area
		        )
		
		Remark: The island working set must be specified using ##WorkingSet##
		
		Remark: [0, 1], 0 will process zero islands while 1 will process all of them
		
		
		PARAMETER       : Orientation
		Brief           : Enable selection and/or copy on the symmetric parts of the islands
		Type            : string
		Possible Values :
		                 - "Straight"        : Process islands having the same topology and same orientation
		                 - "Symmetric"        : Process islands having the same topology with inverted normal orientation (can be the symmetric parts)
		                 - "Both"        : Process both symmetric and straight islands (default)
		
		PARAMETER       : UseUncutTopology
		Brief           : Enable uncut mapping mode
		Type            : bool
		
		If enabled, the original / uncut topology will be used to map primitive and islands instead of use t
		he UV topology.
		
		
		OUTPUT      : Similars
		Brief           : Lists of similar island IDs
		Type            : table
		
		Each int vector contains the list of similar islands indexes
		
		
		OUTPUT      : Edges
		Brief           : Lists of edges that can be used to cut or weld the mesh
		Type            : ints
		
		Will be present only if ##MODE## == "EdgeToCut"
		
		
		PARAMETER       : UseIslandSelection
		Brief           : When specified, the working set will be the selection set
		Type            : bool
		
		If not specified, the island working set will be the visible ones
		
		
		
		"""
		return self.rizomuv.Execute('IslandCopy', p)

	def Uvset(self, p):
		"""
		Manage UVSet
		
		PARAMETER       : Mode
		Brief           : Operation mode selection
		Type            : string
		Default         : "SetCurrent"
		Possible Values :
		                 - "Create"
		                 - "Copy"
		                 - "SetCurrent"
		                 - "Delete"
		
		PARAMETER       : Name
		Brief           : Name of the created or copied or deleted or set as current UVSet
		Type            : string
		
		
		"""
		return self.rizomuv.Execute('Uvset', p)
