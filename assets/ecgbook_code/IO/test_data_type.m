dimfile    = 1;       % dimension of file
seglength  = 1000;    % length of segment we read in each loop
fs=2000;              % sampling frequency
filelength = 10000;   % length of file - redundant
%bintype = 'int16';    % binary type
offset=50;            % offset at start of file that we ignore
noSegs = 1000;        % number of segments to loop over
sillydataseg=35;      % A fudge factor - there seems to be a 35 sample 
                      % drift at each real ECG section  
ecg = [];             % final ecg data vector
noise = [];           % final non-ecg vector

% test for binary file type ....

i=1;
bintype{i} =        'uchar'; i=i+1;
bintype{i} =  	    'schar'  ;i=i+1;
bintype{i} =  	    'int8'    ;i=i+1;
bintype{i} =  	    'int16'  ;i=i+1;
bintype{i} =  	    'int32'   ;i=i+1;
bintype{i} =  	    'int64'  ;i=i+1;
bintype{i} =  	    'uint8'   ;i=i+1;
bintype{i} =  	    'uint16'  ;i=i+1;
bintype{i} =  	    'uint32' ;i=i+1;
bintype{i} =  	    'uint64'  ;i=i+1;
bintype{i} =  	    'single' ;i=i+1;
bintype{i} =  	    'float32' ;i=i+1;
bintype{i} =  	    'double' ;i=i+1;
bintype{i} =          'float64';
 
for(i=1:length(bintype))
 fid = fopen('106.116','rb'); 
 a = fread(fid, [dimfile, filelength], bintype{i}); 
 fclose(fid); 

 for(j=1:dimfile)
  subplot(dimfile,1,j);
   plot(a(j,:));
 end
 subplot(dimfile,1,1);
 title(bintype{i})
 pause
end
