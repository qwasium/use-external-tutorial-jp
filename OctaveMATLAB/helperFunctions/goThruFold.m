classdef goThruFold
    
    properties
        inDir
        outDir
        contentName
        filterStr
        isDir
        dirName
    end % properties
    
    methods
        
        % constructor
        function obj = goThruFold(inDir, outDir, filterStr)
            obj.inDir     = inDir;
            obj.outDir    = outDir;
            obj.filterStr = filterStr;
        end
        
        % main logic: go through files in a folder and apply fileAction()
        function obj = main(obj)
            cd(obj.inDir);
            dirList = dir(obj.inDir);
            dirList = dirList(~cellfun('isempty', {dirList.date})); % date==empty is invalid
            for i = 3:length(dirList)
                cd(obj.inDir)
                obj.contentName = dirList(i).name;
                obj.isDir       = dirList(i).isdir;
                obj.dirName     = dirList(i).folder;
                
                if skipCondition(obj)
                    continue
                end
                cd(obj.dirName)
                fileAction(obj);
            end % for
        end

        function skip = skipCondition(obj)
            skip = false;
            if obj.isDir
                skip = true;
            end
            if ~filterFileName(obj)
                skip = true;
            end
        end
        
        % difine how to filter valid file
        function validity = filterFileName(obj)
            validity = ~isempty(regexp(obj.contentName, obj.filterStr, 'once'));
        end
        
        % define action on file found
        function obj = fileAction(obj)
            fprintf(obj.contentName);
            fprintf('\n');
        end

    end % methods
end % class