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
% ## Compute the Jacobi elliptic functions sn(u|m), cn(u|m) and dn(u|m)
% ## for argument u and parameter m.
% ##
% ## usage: [sn,cn,dn] = ellipj(u,m[,tol])
% ##
% ## u and m must be real arrays of same size.  Either or both can be
% ## scalars. m is restricted to 0 <= m <= 1.
% ##
% ## WARNING: the approximation blows up for abs(U)>20 near m=1.
% ##
% ## tol is accepted for compatibility, but ignored
% ##
% ## Ref: Abramowitz, Milton and Stegun, Irene A
% ##      Handbook of Mathematical Functions, Dover, 1965
% ##      Chapter 16 (Sections 16.4, 16.13 and 16.15)
% ##
% ## Example
% ##    m = linspace(0,1,200); u=linspace(-10,10,200);
% ##    M = ones(length(u),1) * m; U = u' * ones(1,length(m));
% ##    [sn, cn, dn] = ellipj(U,M);
% ##    imagesc(sn);
% ##
% ## See also: ellipke
% 
% ## Author: David Billinghurst <David.Billinghurst@riotinto.com>
% ## Created: 31 January 2001
% ## 2001-02-01 Paul Kienzle
% ##   * vectorized
% ##   * added demos
% ##   * included function name in error messages
% 
function [sn, cn, dn] = ellipj (u, m)

  if nargin < 2 || nargin > 3 
    usage('[sn, cn, dn] = ellipj (u, m)'); 
  end
  if size(u,1) ~= size(m,1) || size(u,2) ~= size(m,2), 
    error('ellipj must have same shape for u and m');
  end

  sn=zeros(size(u));
  cn=zeros(size(u));
  dn=zeros(size(u));
  phi=zeros(size(u));
  m = m(:); u=u(:);

  if ~all(isreal(m) & isreal(u))
    error('ellipj must have real u and m');
  end
  if any(m < 0.0 | m > 1.0), 
    error('ellipj must have m in the range [0,1]');
  end

  lo = sqrt(eps);
  hi = 1-sqrt(eps);

  %dfi = do_fortran_indexing;
  %unwind_protect
  %  do_fortran_indexing = 1;
  
  %  ## For small m, ( Abramowitz and Stegun, Section 16.13 )
    idx = find(m < lo);
    if ~isempty(idx)
      uidx = u(idx);
      midx = m(idx);
      sin_u = sin(uidx);
      cos_u = cos(uidx);
      t = 0.25 * midx .* (uidx - sin_u.*cos_u);
      sn(idx) = sin_u - t.*cos_u;
      cn(idx) = cos_u + t.*sin_u;
      dn(idx) = 1.0 - 0.5*midx.*sin_u.*sin_u;
    end
    
   % ## For m1 = (1-m) small ( Abramowitz and Stegun, Section 16.15 )
    idx = find( m >= hi );
    if ~isempty(idx)
      uidx = u(idx);
      sinh_u = sinh(uidx);
      cosh_u = cosh(uidx);
      tanh_u = tanh(uidx);
      sech_u = 1.0./cosh_u;
      sechm1over4 = 0.25 * (1.0 - m(idx)) ./ cosh_u;
      sinhcosh = sinh_u.*cosh_u;
      sn(idx) = tanh_u + sechm1over4 .* (sinhcosh-uidx) .* sech_u;
      cn(idx) = sech_u - sechm1over4 .* (sinhcosh-uidx) .* tanh_u;
      dn(idx) = sech_u + sechm1over4 .* (sinhcosh+uidx) .* tanh_u;
    end
    
%     ## Arithmetic-Geometric Mean (AGM) algorithm
%     ## ( Abramowitz and Stegun, Section 16.4 )
    idx = find ( lo <= m & m < hi );
    if ~isempty(idx)
      Nmax = 16;
      c = zeros(length(idx),Nmax); 
      a = zeros(length(idx),Nmax);
      a(:,1) = ones(length(idx),1);
      b = sqrt(1.0 - m(idx));
      c(:,1) = sqrt(m(idx));
      for n = 2:Nmax
      	a(:,n) = (a(:,n-1) + b) / 2.0;
      	c(:,n) = (a(:,n-1) - b) / 2.0;
      	b = sqrt ( a(:,n-1) .* b);
      	if all (c(:,n)./a(:,n) < eps), break; 
        end
      end
      if n >= Nmax
      	error('ellipj: Not enough workspace'); 
      end
      phi = 2.^(n-1) * a(:,n) .* u(idx);
      for j=n:-1:2
      	t = phi;
      	phi = ( asin ( (c(:,j)./a(:,j)) .* sin(phi)) + phi ) / 2;
      end
      
      sn(idx) = sin(phi);
      cn(idx) = cos(phi);
      dn(idx) = cos(phi)./cos(t-phi);
    end
%   unwind_protect_cleanup
%     do_fortran_indexing = dfi;
%   end_unwind_protect


%!demo
%! N = 150;
%! % m = [1-logspace(0,log(eps),N-1), 1]; ## m near 1
%! % m = [0, logspace(log(eps),0,N-1)];   ## m near 0
%!   m = linspace(0,1,N);                 ## m equally spaced
%! u = linspace(-20,20,N);
%! M = ones(length(u),1) * m;
%! U = u' * ones(1, length(m));
%! [sn, cn, dn] = ellipj(U,M);
%! c = colormap; colormap(hot(64)); 
%! image(m,u,32*clip(sn,[-1,1])+32,1); 
%! image(m,u,32*clip(cn,[-1,1])+32,1); 
%! image(m,u,32*clip(dn,[-1,1])+32,1);
%! colormap(c);

%!demo
%! N = 200;
%! % m = [1-logspace(0,log(eps),N-1), 1]; ## m near 1
%! % m = [0, logspace(log(eps),0,N-1)];   ## m near 0
%!   m = linspace(0,1,N);                 ## m equally spaced
%! u = linspace(0,20,5);
%! M = ones(length(u),1) * m;
%! U = u' * ones(1, length(m));
%! [sn, cn, dn] = ellipj(U,M);
%! grid("on"); 
%! subplot(131); title("sn"); semilogx(m, sn, ";;");
%! subplot(132); title("cn"); semilogx(m, cn, ";;");
%! subplot(133); title("dn"); semilogx(m, dn, ";;");
%! oneplot; grid("off"); title("");

%!test
%! ## Test Jacobi elliptic functions
%! ## against "exact" solution from Mathematica 3.0
%! ## David Billinghurst <David.Billinghurst@riotinto.com>
%! ## 1 February 2001
%! u = [ 0.25; 0.25; 0.20; 0.20; 0.672; 0.5];
%! m = [ 0.0;  1.0;  0.19; 0.81; 0.36;  0.9999999999];
%! S = [ sin(0.25); tanh(0.25);
%!  0.19842311013970879516;
%!  0.19762082367187648571;
%!  0.6095196917919021945;
%!  0.4621171572617320908 ];
%! C = [ cos(0.25); sech(0.25);
%!  0.9801164570409401062;
%!  0.9802785369736752032;
%!  0.7927709286533560550;
%!  0.8868188839691764094 ];
%! D = [ 1.0;  sech(0.25);
%!  0.9962526643271134302;
%!  0.9840560289645665155;
%!  0.9307281387786906491;
%!  0.8868188839812167635 ];
%! [sn,cn,dn] = ellipj(u,m);
%! assert(sn,S,8*eps);
%! assert(cn,C,8*eps);
%! assert(dn,D,8*eps);
