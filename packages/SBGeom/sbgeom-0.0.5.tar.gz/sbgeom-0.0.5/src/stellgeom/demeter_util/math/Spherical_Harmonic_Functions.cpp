
#include "Constants.h"
#include "Spherical_Harmonic_Functions.h"


std::complex<double> Ylm(int l, int m, const Unit_Vector& Omega_n){
    double theta    = acos(Omega_n[2]);
    double phi      = atan2(Omega_n[1], Omega_n[0]);

    auto pos_ylm    = std::sph_legendre(l ,abs(m), theta)  *sqrt( 4 * Constants::pi) * std::exp(std::complex<double>(0, double(abs(m)) * phi));

    return m >= 0 ? pos_ylm : pow(-1.0, m) * std::conj(pos_ylm);
};

double Ylm_real(lm_real lm, const Unit_Vector& omega_n){
    if(lm.l == 0){
        return Ylm(0,0, omega_n).real();
    }
    else if(! lm.uneven){
        return Ylm(lm.l, lm.m, omega_n).real();
    }
    else{
        return Ylm(lm.l, lm.m, omega_n).imag();
    }
};