import os

from hydrus.core import HydrusConstants as HC
from hydrus.core import HydrusData
from hydrus.core import HydrusExceptions
from hydrus.core import HydrusSerialisable

from hydrus.client.importing.options import ClientImportOptions

class FileImportOptions( HydrusSerialisable.SerialisableBase ):
    
    SERIALISABLE_TYPE = HydrusSerialisable.SERIALISABLE_TYPE_FILE_IMPORT_OPTIONS
    SERIALISABLE_NAME = 'File Import Options'
    SERIALISABLE_VERSION = 5
    
    def __init__( self ):
        
        HydrusSerialisable.SerialisableBase.__init__( self )
        
        self._exclude_deleted = True
        self._do_not_check_known_urls_before_importing = False
        self._do_not_check_hashes_before_importing = False
        self._allow_decompression_bombs = True
        self._min_size = None
        self._max_size = None
        self._max_gif_size = None
        self._min_resolution = None
        self._max_resolution = None
        self._automatic_archive = False
        self._associate_primary_urls = True
        self._associate_source_urls = True
        self._present_new_files = True
        self._present_already_in_inbox_files = True
        self._present_already_in_archive_files = True
        
    
    def _GetSerialisableInfo( self ):
        
        pre_import_options = ( self._exclude_deleted, self._do_not_check_known_urls_before_importing, self._do_not_check_hashes_before_importing, self._allow_decompression_bombs, self._min_size, self._max_size, self._max_gif_size, self._min_resolution, self._max_resolution )
        post_import_options = ( self._automatic_archive, self._associate_primary_urls, self._associate_source_urls )
        presentation_options = ( self._present_new_files, self._present_already_in_inbox_files, self._present_already_in_archive_files )
        
        return ( pre_import_options, post_import_options, presentation_options )
        
    
    def _InitialiseFromSerialisableInfo( self, serialisable_info ):
        
        ( pre_import_options, post_import_options, presentation_options ) = serialisable_info
        
        ( self._exclude_deleted, self._do_not_check_known_urls_before_importing, self._do_not_check_hashes_before_importing, self._allow_decompression_bombs, self._min_size, self._max_size, self._max_gif_size, self._min_resolution, self._max_resolution ) = pre_import_options
        ( self._automatic_archive, self._associate_primary_urls, self._associate_source_urls ) = post_import_options
        ( self._present_new_files, self._present_already_in_inbox_files, self._present_already_in_archive_files ) = presentation_options 
        
    
    def _UpdateSerialisableInfo( self, version, old_serialisable_info ):
        
        if version == 1:
            
            ( automatic_archive, exclude_deleted, min_size, min_resolution ) = old_serialisable_info
            
            present_new_files = True
            present_already_in_inbox_files = False
            present_already_in_archive_files = False
            
            new_serialisable_info = ( automatic_archive, exclude_deleted, present_new_files, present_already_in_inbox_files, present_already_in_archive_files, min_size, min_resolution )
            
            return ( 2, new_serialisable_info )
            
        
        if version == 2:
            
            ( automatic_archive, exclude_deleted, present_new_files, present_already_in_inbox_files, present_already_in_archive_files, min_size, min_resolution ) = old_serialisable_info
            
            max_size = None
            max_resolution = None
            
            allow_decompression_bombs = True
            max_gif_size = 32 * 1048576
            
            pre_import_options = ( exclude_deleted, allow_decompression_bombs, min_size, max_size, max_gif_size, min_resolution, max_resolution )
            post_import_options = automatic_archive
            presentation_options = ( present_new_files, present_already_in_inbox_files, present_already_in_archive_files )
            
            new_serialisable_info = ( pre_import_options, post_import_options, presentation_options )
            
            return ( 3, new_serialisable_info )
            
        
        if version == 3:
            
            ( pre_import_options, post_import_options, presentation_options ) = old_serialisable_info
            
            ( exclude_deleted, allow_decompression_bombs, min_size, max_size, max_gif_size, min_resolution, max_resolution ) = pre_import_options
            
            automatic_archive = post_import_options
            
            do_not_check_known_urls_before_importing = False
            do_not_check_hashes_before_importing = False
            associate_source_urls = True
            
            pre_import_options = ( exclude_deleted, do_not_check_known_urls_before_importing, do_not_check_hashes_before_importing, allow_decompression_bombs, min_size, max_size, max_gif_size, min_resolution, max_resolution )
            
            post_import_options = ( automatic_archive, associate_source_urls )
            
            new_serialisable_info = ( pre_import_options, post_import_options, presentation_options )
            
            return ( 4, new_serialisable_info )
            
        
        if version == 4:
            
            ( pre_import_options, post_import_options, presentation_options ) = old_serialisable_info
            
            ( automatic_archive, associate_source_urls ) = post_import_options
            
            associate_primary_urls = True
            
            post_import_options = ( automatic_archive, associate_primary_urls, associate_source_urls )
            
            new_serialisable_info = ( pre_import_options, post_import_options, presentation_options )
            
            return ( 5, new_serialisable_info )
            
        
    
    def AllowsDecompressionBombs( self ):
        
        return self._allow_decompression_bombs
        
    
    def AutomaticallyArchives( self ) -> bool:
        
        return self._automatic_archive
        
    
    def CheckFileIsValid( self, size, mime, width, height ):
        
        if self._min_size is not None and size < self._min_size:
            
            raise HydrusExceptions.FileSizeException( 'File was ' + HydrusData.ToHumanBytes( size ) + ' but the lower limit is ' + HydrusData.ToHumanBytes( self._min_size ) + '.' )
            
        
        if self._max_size is not None and size > self._max_size:
            
            raise HydrusExceptions.FileSizeException( 'File was ' + HydrusData.ToHumanBytes( size ) + ' but the upper limit is ' + HydrusData.ToHumanBytes( self._max_size ) + '.' )
            
        
        if mime == HC.IMAGE_GIF and self._max_gif_size is not None and size > self._max_gif_size:
            
            raise HydrusExceptions.FileSizeException( 'File was ' + HydrusData.ToHumanBytes( size ) + ' but the upper limit for gifs is ' + HydrusData.ToHumanBytes( self._max_gif_size ) + '.' )
            
        
        if self._min_resolution is not None:
            
            ( min_width, min_height ) = self._min_resolution
            
            too_thin = width is not None and width < min_width
            too_short = height is not None and height < min_height
            
            if too_thin or too_short:
                
                raise HydrusExceptions.FileSizeException( 'File had resolution ' + HydrusData.ConvertResolutionToPrettyString( ( width, height ) ) + ' but the lower limit is ' + HydrusData.ConvertResolutionToPrettyString( self._min_resolution ) )
                
            
        
        if self._max_resolution is not None:
            
            ( max_width, max_height ) = self._max_resolution
            
            too_wide = width is not None and width > max_width
            too_tall = height is not None and height > max_height
            
            if too_wide or too_tall:
                
                raise HydrusExceptions.FileSizeException( 'File had resolution ' + HydrusData.ConvertResolutionToPrettyString( ( width, height ) ) + ' but the upper limit is ' + HydrusData.ConvertResolutionToPrettyString( self._max_resolution ) )
                
            
        
    
    def CheckNetworkDownload( self, possible_mime, num_bytes, is_complete_file_size ):
        
        if is_complete_file_size:
            
            error_prefix = 'Download was apparently '
            
        else:
            
            error_prefix = 'Download was at least '
            
        
        if possible_mime is not None:
            
            if possible_mime == HC.IMAGE_GIF and self._max_gif_size is not None and num_bytes > self._max_gif_size:
                
                raise HydrusExceptions.FileSizeException( error_prefix + HydrusData.ToHumanBytes( num_bytes ) + ' but the upper limit for gifs is ' + HydrusData.ToHumanBytes( self._max_gif_size ) + '.' )
                
            
        
        if self._max_size is not None and num_bytes > self._max_size:
            
            raise HydrusExceptions.FileSizeException( error_prefix + HydrusData.ToHumanBytes( num_bytes ) + ' but the upper limit is ' + HydrusData.ToHumanBytes( self._max_size ) + '.' )
            
        
        if is_complete_file_size:
            
            if self._min_size is not None and num_bytes < self._min_size:
                
                raise HydrusExceptions.FileSizeException( error_prefix + HydrusData.ToHumanBytes( num_bytes ) + ' but the lower limit is ' + HydrusData.ToHumanBytes( self._min_size ) + '.' )
                
            
        
    
    def ExcludesDeleted( self ):
        
        return self._exclude_deleted
        
    
    def GetPresentationOptions( self ):
        
        presentation_options = ( self._present_new_files, self._present_already_in_inbox_files, self._present_already_in_archive_files )
        
        return presentation_options
        
    
    def GetPreImportOptions( self ):
        
        pre_import_options = ( self._exclude_deleted, self._do_not_check_known_urls_before_importing, self._do_not_check_hashes_before_importing, self._allow_decompression_bombs, self._min_size, self._max_size, self._max_gif_size, self._min_resolution, self._max_resolution )
        
        return pre_import_options
        
    
    def GetSummary( self ):
        
        statements = []
        
        if self._exclude_deleted:
            
            statements.append( 'excluding previously deleted' )
            
        
        if not self._allow_decompression_bombs:
            
            statements.append( 'excluding decompression bombs' )
            
        
        if self._min_size is not None:
            
            statements.append( 'excluding < ' + HydrusData.ToHumanBytes( self._min_size ) )
            
        
        if self._max_size is not None:
            
            statements.append( 'excluding > ' + HydrusData.ToHumanBytes( self._max_size ) )
            
        
        if self._max_gif_size is not None:
            
            statements.append( 'excluding gifs > ' + HydrusData.ToHumanBytes( self._max_gif_size ) )
            
        
        if self._min_resolution is not None:
            
            ( width, height ) = self._min_resolution
            
            statements.append( 'excluding < ( ' + HydrusData.ToHumanInt( width ) + ' x ' + HydrusData.ToHumanInt( height ) + ' )' )
            
        
        if self._max_resolution is not None:
            
            ( width, height ) = self._max_resolution
            
            statements.append( 'excluding > ( ' + HydrusData.ToHumanInt( width ) + ' x ' + HydrusData.ToHumanInt( height ) + ' )' )
            
        
        #
        
        if self._automatic_archive:
            
            statements.append( 'automatically archiving' )
            
        
        #
        
        presentation_statements = []
        
        if self._present_new_files:
            
            presentation_statements.append( 'new' )
            
        
        if self._present_already_in_inbox_files:
            
            presentation_statements.append( 'already in inbox' )
            
        
        if self._present_already_in_archive_files:
            
            presentation_statements.append( 'already in archive' )
            
        
        if len( presentation_statements ) == 0:
            
            statements.append( 'not presenting any files' )
            
        elif len( presentation_statements ) == 3:
            
            statements.append( 'presenting all files' )
            
        else:
            
            statements.append( 'presenting ' + ', '.join( presentation_statements ) + ' files' )
            
        
        summary = os.linesep.join( statements )
        
        return summary
        
    
    def SetPostImportOptions( self, automatic_archive: bool, associate_primary_urls: bool, associate_source_urls: bool ):
        
        self._automatic_archive = automatic_archive
        self._associate_primary_urls = associate_primary_urls
        self._associate_source_urls = associate_source_urls
        
    
    def SetPresentationOptions( self, present_new_files, present_already_in_inbox_files, present_already_in_archive_files ):
        
        self._present_new_files = present_new_files
        self._present_already_in_inbox_files = present_already_in_inbox_files
        self._present_already_in_archive_files = present_already_in_archive_files
        
    
    def SetPreImportOptions( self, exclude_deleted, do_not_check_known_urls_before_importing, do_not_check_hashes_before_importing, allow_decompression_bombs, min_size, max_size, max_gif_size, min_resolution, max_resolution ):
        
        self._exclude_deleted = exclude_deleted
        self._do_not_check_known_urls_before_importing = do_not_check_known_urls_before_importing
        self._do_not_check_hashes_before_importing = do_not_check_hashes_before_importing
        self._allow_decompression_bombs = allow_decompression_bombs
        self._min_size = min_size
        self._max_size = max_size
        self._max_gif_size = max_gif_size
        self._min_resolution = min_resolution
        self._max_resolution = max_resolution
        
    
    def ShouldAssociatePrimaryURLs( self ) -> bool:
        
        return self._associate_primary_urls
        
    
    def ShouldAssociateSourceURLs( self ) -> bool:
        
        return self._associate_source_urls
        
    
    def DoNotCheckHashesBeforeImporting( self ):
        
        return self._do_not_check_hashes_before_importing
        
    
    def DoNotCheckKnownURLsBeforeImporting( self ):
        
        return self._do_not_check_known_urls_before_importing
        
    
    def ShouldNotPresentIgnorantOfInbox( self, status ):
        
        return ClientImportOptions.NewInboxArchiveNonMatchIgnorantOfInbox( self._present_new_files, self._present_already_in_inbox_files, self._present_already_in_archive_files, status )
        
    
    def ShouldPresent( self, status, inbox ):
        
        return ClientImportOptions.NewInboxArchiveMatch( self._present_new_files, self._present_already_in_inbox_files, self._present_already_in_archive_files, status, inbox )
        
    
    def ShouldPresentIgnorantOfInbox( self, status ):
        
        return ClientImportOptions.NewInboxArchiveMatchIgnorantOfInbox( self._present_new_files, self._present_already_in_inbox_files, self._present_already_in_archive_files, status )
        
    
HydrusSerialisable.SERIALISABLE_TYPES_TO_OBJECT_TYPES[ HydrusSerialisable.SERIALISABLE_TYPE_FILE_IMPORT_OPTIONS ] = FileImportOptions
