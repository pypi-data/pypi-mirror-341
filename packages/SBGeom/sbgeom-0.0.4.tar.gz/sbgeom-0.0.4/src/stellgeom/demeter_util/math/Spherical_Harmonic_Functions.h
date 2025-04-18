#pragma once 
#include <cmath>
#include <complex>
#include "Vector.h"
#include "Contiguous_Arrays.h"
/**
 * @brief Spherical harmonic function \f$Y_{lm}\f$
 *
 *  Uses the following definition:
 * \f[Y_{lm}(\theta, \phi) = \sqrt{\frac{(2l+1)(l-m)!}{(l+m)!}} P^m_l(\cos(\theta)) e^{i \phi m} \f]
 *  
 *  @param l 
 *  @param m 
 *  @param Omega_n
 *
 */
std::complex<double> Ylm(int l, int m, const Unit_Vector& Omega_n);

/**
 * @brief Struct for encapsulating a (l,m) pair for spherical harmonics
 * 
 */
struct lm{
    /**
     * @brief Construct a new lm object
     * 
     * @param l_in 
     * @param m_in 
     */
    lm(int l_in, int m_in) : l(l_in), m(m_in){}

    /**
     * @brief \f$l\f$
     * 
     */
    int l;
    
    /**
     * @brief \f$m\f$
     * 
     */
    int m;

    /**
     * @brief Comparison operator
     * 
     * @param lm_other 
     * @return true 
     * @return false 
     */
    bool operator==(lm lm_other)const{return lm_other.l == l && lm_other.m == m;}
};

/**
 * @brief Templated class to iterate over all (l,m) pairs for a given maximum order
 * 
 * 
 * Use simply as \code{.cpp} for(auto lm : lm_iterator<L>()){...} \endcode
 * 
 * @tparam L 
 */
template<unsigned L>
class lm_iterator{
    public:
        class iterator : public std::iterator<std::input_iterator_tag, lm, lm,const lm*, lm>{
            int m_l_order = 0;
            lm current_lm = lm(0,0);
            public:
            explicit iterator(int legendre_order, lm lm_in = lm(0,0)) : current_lm(lm_in), m_l_order(legendre_order) {}
            iterator& operator++() { 
                if(current_lm.m == current_lm.l){ 
                    current_lm.l += 1;
                    current_lm.m = - current_lm.l;
                }
                else{
                    current_lm.m += 1;                   
                }
                return *this;
            }
            iterator operator++(int) { iterator retval = *this; ++(*this); return retval;}
            bool operator==(iterator other) const { return current_lm == other.current_lm;}
            bool operator!=(iterator other) const { return !(*this == other);}
            reference operator*() const{ return current_lm;}
    };
    lm_iterator(){}
    iterator begin(){return iterator(L, lm(0,0));}
    iterator end()  {return iterator(L, lm(L + 1 , - (L+1)));}
};

/**
 * @brief Templated class to store a complete collection data of all pairs (l,m)
 * 
 * @tparam T datatype to store
 * @tparam L maximum legendre order
 */
template<class T, unsigned L>
class X_lm{
    public:
        /**
         * @brief Construct a new x lm collection object
         * 
         * Template L determines underlying array size
         * 
         */
        X_lm() : m_data((1+ L)  * (1 + L))     {m_data.setZero();}
        
        T operator() (lm lm_in)           const{return m_data(this->lm_index(lm_in.l, lm_in.m));}
        T& operator()(lm lm_in)                {return m_data(this->lm_index(lm_in.l, lm_in.m));}

        T operator() (size_t l, size_t m) const{return m_data(this->lm_index(l,m));}
        T& operator()(size_t l, size_t m)      {return m_data(this->lm_index(l,m));}

        /**
         * @brief Write out complete dataset
         * 
         */
        void Write() const{
            for(auto lm_i : lm_iterator<L>()){
                std::cout<<lm_i.l<<","<<lm_i.m<<","<<this->Get_lm(lm_i.l,lm_i.m)<<std::endl;
            }
        }
    private:
        Eigen::Array<T,Eigen::Dynamic, 1> m_data;
        size_t lm_index(int l, int m) const{
           sb_assert(l <= L && m >= -l && m <= l);
           return size_t(l * l  + l + m );
        };
        
};

/**
 * @brief Templated class to store a complete collection data of all indices (i,l,m) 
 * 
 * i represents an external index (e.g. list of nodes)
 * 
 * 
 * 
 * @tparam T datatype
 * @tparam L maximum legendre order
 */
template<class T, unsigned L>
class X_ilm{
    public:

        /**
         * @brief Construct a new x i lm collection object
         * 
         * @param i_number number of external indices
         */
        X_ilm(size_t i_number) : m_data(i_number, (1+ L)  * (1 + L)) { m_data.setZero();};        

        void Set_i_with_X_lm(const X_lm<T,L>& x_lm_in, int i){
            for(auto lm_i : lm_iterator<L>()){
                this->operator()(i,lm_i) = x_lm_in(lm_i);
            }
        }
        void Conj(){
            m_data = m_data.conjugate();
        }
        void Set_Zero(){m_data.setZero();}

        /**
         * @brief Gets maximum number of external indices
         * 
         * @return unsigned 
         */
        unsigned Get_Number_Values() const{return m_data.rows();}


        T  operator() (size_t i, lm lm_in)     const{ return m_data(i, this->lm_index(lm_in.l, lm_in.m));}
        T& operator() (size_t i, lm lm_in)          { return m_data(i, this->lm_index(lm_in.l, lm_in.m));}

        T  operator() (size_t i, int l, int m) const{ return m_data(i, this->lm_index(l,m));}
        T& operator() (size_t i, int l, int m)      { return m_data(i, this->lm_index(l,m));}
                
        /**
         * @brief Function for obtaining a 3d matrix of all the data (real part)
         * The 3D matrix is a bit weird: the m index is just shifted towards the first index:
         * i.e. for a l=2 matrix we have (l,m) (at fixed node i)
         * [(0,  0),     0.0,     0.0,     0.0,     0.0]
         * [(1, -1), (1,  0), (1,  1),     0.0,     0.0]
         * [(2, -2), (2, -1), (2,  0), (2,  1), (2,  2)]
         * @return std::unique_ptr<Contiguous3D<T>> 
         */
        std::unique_ptr<Contiguous3D<T>> Obtain_3D_Matrix(){
            auto result = std::make_unique<Contiguous3D<T>>(m_data.rows(), L + 1, 2* L  + 1);
            for(int i  = 0; i < m_data.rows(); ++i){
                for(int l = 0; l<= L; ++l){
                    for(int m = -l; m <= l; ++m){
                        (*result)(i,l, m +l) = this->operator()(i, l, m);
                    }
                }
            }
            return result;
        }

        Eigen::Matrix<T, Eigen::Dynamic, Eigen::Dynamic, Eigen::RowMajor> Return_2D_Matrix() const{
            return m_data;
        }

        Eigen::Array<T, Eigen::Dynamic, 1> Return_1D_Vector() const{
            return m_data.template reshaped<Eigen::RowMajor>();
        }


        Eigen::Array<T, Eigen::Dynamic, 1> Return_lm_Total(lm lm_in) const{return m_data.col(this->lm_index(lm_in.l, lm_in.m));}

        Eigen::Array<T,Eigen::Dynamic, Eigen::Dynamic, Eigen::RowMajor> m_data;

    private:
        
        // For locality, computing types of Psi_lmg it sums over i and thus that should be the fastest changing index ? this is not the case?
        size_t lm_index(int l, int m) const{
           sb_assert(l <= L && m >= -l && m <= l);
            return size_t(l * l  + l + m);
        };          
};

class lm_real
{
    public:
    lm_real(int l_in, unsigned m_in, bool uneven_in) : l(l_in), m(m_in), uneven(uneven_in){}

    size_t index() const {
        if(m == 0){
            return l * l;
        }
        else if(uneven){
            return l * l + l + m;
        }
        else{
            return l * l + m;
        }
    }


    int l;
    unsigned m ;
    bool uneven ;

    bool operator==(lm_real lm_other)const{return lm_other.l == l && lm_other.m == m && lm_other.uneven == uneven;}

    
};

double Ylm_real(lm_real lm, const Unit_Vector& omega_n);

/**
 * @brief Templated class to iterate over all (l,m) pairs for a given maximum order
 * 
 * 
 * Use simply as \code{.cpp} for(auto lm : lm_iterator<L>()){...} \endcode
 * 
 * @tparam L 
 */
template<unsigned L>
class Real_lm_iterator{
    public:
        class iterator : public std::iterator<std::input_iterator_tag, lm_real, lm_real ,const lm_real*, lm_real>{
            int m_l_order = 0;
            lm_real current_lm = lm_real(0,0, false);
            public:
            explicit iterator(int legendre_order, lm_real lm_in = lm_real(0,0)) : current_lm(lm_in), m_l_order(legendre_order) {}
            iterator& operator++() { 
                if(current_lm.l ==0){
                    current_lm.l += 1;
                    current_lm.m = 0;
                    current_lm.uneven = false;
                }
                else if(current_lm.m == current_lm.l && current_lm.uneven){ 
                    current_lm.l += 1;
                    current_lm.m = 0;
                    current_lm.uneven = false;
                }
                else if(current_lm.m == current_lm.l && ! current_lm.uneven){
                    current_lm.m = 1;
                    current_lm.uneven = true;
                }
                else{
                    current_lm.m += 1;                   
                }
                return *this;
            }
            iterator operator++(int) { iterator retval = *this; ++(*this); return retval;}
            bool operator==(iterator other) const { return current_lm == other.current_lm;}
            bool operator!=(iterator other) const { return !(*this == other);}
            reference operator*() const{ return current_lm;}
    };
    Real_lm_iterator(){}
    iterator begin(){return iterator(L, lm_real(0,0, false));}
    iterator end()  {return iterator(L, lm_real(L + 1 , 0, false));}
};

template<typename T>
class RealSphericalHarmonicExpansion_Wrapper{
    public:

    RealSphericalHarmonicExpansion_Wrapper(size_t number_of_values) : m_number_of_values(number_of_values) {};
    
    virtual Eigen::Map<Eigen::Matrix<T, Eigen::Dynamic, Eigen::Dynamic, Eigen::RowMajor>> Matrix_2D() = 0 ;
    virtual Eigen::Map<const Eigen::Matrix<T, Eigen::Dynamic, Eigen::Dynamic, Eigen::RowMajor>> Matrix_2D() const = 0 ;
        
    

    virtual T& operator()(size_t j, lm_real lm) = 0;
    virtual const T& operator()(size_t j, lm_real lm) const = 0 ;

    virtual unsigned L () const = 0;

    size_t Number_of_Values() const {return m_number_of_values;};
    
    virtual ~RealSphericalHarmonicExpansion_Wrapper(){}

    virtual const Eigen::Vector<T, Eigen::Dynamic>& Data() const = 0 ;
    protected:
    size_t m_number_of_values;

    


};

template<typename T, unsigned L_order>
class RealSphericalHarmonicExpansion : public RealSphericalHarmonicExpansion_Wrapper<T>{
    public:

    RealSphericalHarmonicExpansion(size_t number_of_values) : RealSphericalHarmonicExpansion_Wrapper<T>(number_of_values), m_data(number_of_values * ( L_order +1 ) * (L_order + 1)) , \
                                                                                                                          m_lm_values((L_order + 1) * (L_order+ 1))
    {};

    RealSphericalHarmonicExpansion(const RealSphericalHarmonicExpansion<T, L_order>& copy_in) : RealSphericalHarmonicExpansion_Wrapper<T>(copy_in.Number_of_Values()), m_data(copy_in.m_data), \
                                                                                                                          m_lm_values(copy_in.m_lm_values)
    {};

    RealSphericalHarmonicExpansion(RealSphericalHarmonicExpansion<T, L_order>&& copy_in) : RealSphericalHarmonicExpansion_Wrapper<T>(copy_in.Number_of_Values()), m_lm_values(copy_in.m_lm_values), m_data(std::move(copy_in.m_data))                                                                                   
    {};

    RealSphericalHarmonicExpansion<T, L_order>& operator=(const RealSphericalHarmonicExpansion<T, L_order>& other){
        this->m_lm_values = other.m_lm_values;
        this->m_data = other.m_data;
        this->m_number_of_values = other.m_number_of_values;        
        return *this;
    }

    
    Eigen::Map<Eigen::Matrix<T, Eigen::Dynamic, Eigen::Dynamic, Eigen::RowMajor>> Matrix_2D(){
        
        return Eigen::Map<Eigen::Matrix<T, Eigen::Dynamic, Eigen::Dynamic, Eigen::RowMajor>>(m_data.data(), this->m_number_of_values, m_lm_values);
    }
    Eigen::Map<const Eigen::Matrix<T, Eigen::Dynamic, Eigen::Dynamic, Eigen::RowMajor>> Matrix_2D() const {
        return Eigen::Map<const Eigen::Matrix<T, Eigen::Dynamic, Eigen::Dynamic, Eigen::RowMajor>>(m_data.data(), this->m_number_of_values, m_lm_values);
    }

    void Set_Data(const Eigen::Array<T, Eigen::Dynamic, Eigen::Dynamic, Eigen::RowMajor>& data){
        sb_assert_message(data.rows() == this->Number_of_Values(), "Number of rows (" +std::to_string(data.rows()) +") does not match number of values of RealSphericalHarmonicExpansion ("+std::to_string(this->Number_of_Values())+")");
        sb_assert_message(data.cols() == this->m_lm_values, "Number of columns (" +std::to_string(data.cols()) +") does not match number of lm values of RealSphericalHarmonicExpansion ("+std::to_string(this->m_lm_values)+")");
        Eigen::Map<const Eigen::Vector<T, Eigen::Dynamic>> map_result = Eigen::Map<const Eigen::Vector<T, Eigen::Dynamic>>(data.data(), this->Number_of_Values() * this->m_lm_values);
        m_data = map_result;
    }

    const T* jBlock_start(size_t j) const {return &m_data(j * m_lm_values);}
    T& operator()(size_t j, lm_real lm){return m_data(j * m_lm_values + lm.index());}
    const T& operator()(size_t j, lm_real lm) const {return m_data(j * m_lm_values + lm.index());}
    
    unsigned L() const override{return L_order;}
    
    const Eigen::Vector<T, Eigen::Dynamic>& Data() const {return m_data;}

    Eigen::Vector<T, Eigen::Dynamic>& Data(){return m_data;}

    protected:

    Eigen::Vector<T, Eigen::Dynamic> m_data;    
    size_t m_lm_values ; 
    


};