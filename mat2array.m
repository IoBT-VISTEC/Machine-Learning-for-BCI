function a = mat2array(x, shape, dtype)

if nargin < 2|| isempty(shape)
    shape = size(x);
end
if nargin < 3
    dtype = py.None;
end

a = py.numpy.array(x(:)', dtype).reshape(shape);