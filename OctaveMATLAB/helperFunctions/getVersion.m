function [isOctave, runningVersion] = getVersion()
% GETVERSION get the MATLAB/Octave version its running on
% Aug2023 SK 
% 
% return:
%   - isOctave       (bool)       GNU/Octave==TRUE, MATLAB==FALSE
%   - isNewer        (bool)       Same/newer/no args==TRUE, older==FALSE 
%   - runningVersion (cell array) See examples below.
%                              Octave: {'6.4.1'}   {'6'} {'4'} {'1'}
%                              MATLAB: {version()} {'2022'} {'a'}
%              MATLAB(parsing failed): {version()} {version('-release')}
%                                   
% CAUTION: 
%   - It might behave broken depending on changes made by matlab or octave.
%   - These changes are out of control of the end user.
%   - Not meant to be used for legacy versions(untested).
%   - Very old versions will probably fail or return garbage.

    isOctave = exist('OCTAVE_VERSION', 'builtin')~=0;
    
    if isOctave
        octaveVer      = version();
        runningVersion = {octaveVer};
        verSplit       = regexp(octaveVer, '\.', 'split');
        verSz          = size(verSplit);
        for i = 1:verSz(2)
            runningVersion{i+1} = char(verSplit(i));
        end

    else
        matlabVer      = version('-release');
        runningVersion = {version(), matlabVer};

        % release version must be 5 charactors long (example:2021b)
        verSz = size(matlabVer);
        if verSz(2) ~= 5
            return
        end
        
        % devede relese version into year + a/b
        filter               = '^\d{4}'; % start with 4 numeric digits
        [verYear, verSuffix] = regexp(matlabVer, filter, 'match', 'split');
        verSuffix            = verSuffix(2);
        
        % reject if not devided into yyyy + a/b
        if isempty(verYear)
            return
        end
        if ~(char(verSuffix) == 'a' || char(verSuffix) == 'b')
            return
        end
        
        % return
        runningVersion = {version(), char(verYear), char(verSuffix)};

    end % if isOctave
end % function



