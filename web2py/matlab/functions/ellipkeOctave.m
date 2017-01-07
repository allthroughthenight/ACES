% ## Copyright (C) 2001 David Billinghurst
% ##
% ## This program is free software; you can redistribute it and/or modify
% ## it under the terms of the GNU General Public License as published by
% ## the Free Software Foundation; either version 2 of the License, or   
% ## (at your option) any later version.
% ##
% ## This program is distributed in the hope that it will be useful,
% ## but WITHOUT ANY WARRANTY; without even the implied warranty of
% ## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
% ## GNU General Public License for more details.
% ##
% ## You should have received a copy of the GNU General Public License
% ## along with this program; if not, write to the Free Software
% ## Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
% 
% ## Compute:
% ##     complete elliptic integral of first K(m) 
% ##     complete elliptic integral of second E(m)    
% ##
% ## usage: [k,e] = ellipke(m[,tol])
% ## 
% ## m is either real array or scalar with 0 <= m <= 1
% ## 
% ## tol  Ignored. 
% ##      (Matlab uses this to allow faster, less accurate approximation)
% ##
% ## Ref: Abramowitz, Milton and Stegun, Irene A
% ##      Handbook of Mathematical Functions, Dover, 1965
% ##      Chapter 17
% ##
% ## See also: ellipj
% 
% ## Author: David Billinghurst <David.Billinghurst@riotinto.com>
% ## Created: 31 January 2001
% ## 2001-02-01 Paul Kienzle
% ##   * vectorized
% ##   * included function name in error messages

function [k,e] = ellipke( m )

  if (nargin < 1 || nargin > 2)
    usage('[k, e] = ellipke (m)');
  end

  k = zeros(size(m));
  e = zeros(size(m));
 
  m = m(:);
  if any(~isreal(m))
    error('ellipke must have real m'); 
  end
  if any(m<0) || any(m>1)
    error('ellipke must have m in the range [0,1]');
  end
  
  
  Nmax = 16;
%  dfi = do_fortran_indexing;
%  unwind_protect
%    do_fortran_indexing = 1;

    idx = find(m == 1);
    if (~isempty(idx))
      k(idx) = Inf;
      e(idx) = 1.0;
    end

%     ## Arithmetic-Geometric Mean (AGM) algorithm
%     ## ( Abramowitz and Stegun, Section 17.6 )
    idx = find(m ~= 1);
    if (~isempty(idx))
      a = ones(length(idx),1);
      b = sqrt(1.0-m(idx));
      c = sqrt(m(idx));
      f = 0.5;
      sum = f*c.*c;
      for n = 2:Nmax
        t = (a+b)/2;
        c = (a-b)/2;
        b = sqrt(a.*b);
        a = t;
        f = f * 2;
        sum = sum + f*c.*c;
        if all(c./a < eps), break;
        end
       end
      if n >= Nmax, error('ellipke: not enough workspace'); end
      k(idx) = 0.5*pi./a;
      e(idx) = 0.5*pi.*(1.0-sum)./a;
     end
 % unwind_protect_cleanup
 %   do_fortran_indexing = dfi;
 % end_unwind_protect

        

%!test
%! ## Test complete elliptic functions of first and second kind
%! ## against "exact" solution from Mathematica 3.0
%! ##
%! ## David Billinghurst <David.Billinghurst@riotinto.com>
%! ## 1 February 2001
%! m = [0.0; 0.01; 0.1; 0.5; 0.9; 0.99; 1.0 ];
%! [k,e] = ellipke(m);
%!
%! # K(1.0) is really infinity - see below
%! K = [ 
%!  1.5707963267948966192;
%!  1.5747455615173559527;
%!  1.6124413487202193982;
%!  1.8540746773013719184;
%!  2.5780921133481731882;
%!  3.6956373629898746778;
%!  0.0 ];
%! E = [
%!  1.5707963267948966192;
%!  1.5668619420216682912;
%!  1.5307576368977632025;
%!  1.3506438810476755025;
%!  1.1047747327040733261;
%!  1.0159935450252239356;
%!  1.0 ];
%! if k(7)==Inf, k(7)=0.0; end;
%! assert(K,k,8*eps);
%! assert(E,e,8*eps);
