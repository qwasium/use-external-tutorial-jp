classdef searchAndDestroy < goThruFold
% Search folder and delete any file matching file name
% Will fail if don't have privileges for write protection.
    methods
        % constructor
        function obj = searchAndDestroy(inDir, outDir, filterStr)
            obj@goThruFold(inDir, outDir, filterStr);
        end
        
        % action on file: destroy
        function obj = fileAction(obj)
            cd(obj.dirName)
            delete(obj.contentName);
        end
    end % methods
end % class

