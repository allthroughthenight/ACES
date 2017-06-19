function [ rhs ] = FWTEQNS( d, L, z, Hoverd, n, Hnon, dpi, celdef, unon, cosa, sina )
%Evaluate the equations: give right hand side term

    rhs = zeros(1, 8);

    if d/L<1.5
        rhs(1) = z(2)-z(1)*Hoverd;
        rhs(5) = rhs(5) - z(8)/z(1);
        for i = 1:n
            coeff(i)  = z(n+i+10) / cosh(i*z(1));
        end
    else
        rhs(1) = z(1) + 1;
    end
    
    rhs(2) = z(2)-Hnon*z(3)^2;
    rhs(3) = z(4) * z(3) - 2*dpi;
    rhs(4) = z(5) + z(7) - z(4);
    rhs(5) = z(6) + z(7) - z(4);
     
    if celdef ==1
        it = 5;
    else 
        it = 6;
    end
    rhs(6) = z(it) - unon*sqrt(z(2));
    rhs(7) = z(10) + z(n+10);
    
    for i = 1:n-1
       rhs(7) = rhs(7) + z(10+i) + z(10+i);
    end
    rhs(8) = z(10) - z(n+10) - z(2);
    
    for m = 1:n
        psi= 0;
        u = 0;
        v = 0;
        if d/L<1.5
            for j = 2:n
                nm  = mod(m*j, n+n) + 1;
                e   = exp(j*(z(1) + z(10+m)));
                s   = 0.5 * (e-1./e);
                c   = 0.5 * (e+1./e);
                psi = psi + coeff(j) * s * cosa(nm);
                u   = u + j*coeff(j) * c * cosa(nm);
                v   = v + j*coeff(j) * s * sina(nm);
            end
        else
            for j = 2:n
                nm  = mod(m*j, n+n) + 1;
                e   = exp(j*z(10+m));
                psi = psi + z(n+j+10) * e * cosa(nm);
                u   = u + j*z(n+j+10) * e * cosa(nm);
                v   = v + j*z(n+j+10) * e * sina(nm);
            end
        end
        rhs(m+9)    = psi - z(8) - z(7)*z(m+10);
        rhs(n+m+10) = 0.5 * ((u-z(7))^2 + v^2) + z(m+10) - z(9);
    end

end

