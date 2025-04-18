#pragma once
#include <memory>
#include "custom_assert.h"
#include <iostream>

/**
 * @brief Contiguous 3D array
 * 
 * @tparam T 
 */
template <class T>
class Contiguous3D{
    public:
        Contiguous3D(size_t n_first, size_t n_second, size_t n_third) : m_n_first(n_first), m_n_second(n_second), m_n_third(n_third), m_data(std::make_unique<T[]>(n_first * n_second * n_third)), m_first_stride(n_second * n_third), m_second_stride(n_third){};
        

        T  operator()(size_t i1, size_t i2, size_t i3) const {sb_assert(i1 < m_n_first && i2 < m_n_second && i3 < m_n_third && "Index out of range for Contiguous3D array"); return m_data[i1 * m_n_second * m_n_third + i2 * m_n_third + i3];}
        T& operator()(size_t i1, size_t i2, size_t i3)       {sb_assert(i1 < m_n_first && i2 < m_n_second && i3 < m_n_third && "Index out of range for Contiguous3D array"); return m_data[i1 * m_n_second * m_n_third + i2 * m_n_third + i3];}

        const T* Pointer(size_t i1, size_t i2, size_t i3) const{sb_assert(i1 < m_n_first && i2 < m_n_second && i3 < m_n_third && "Index out of range for Contiguous3D array"); return &m_data[i1 * m_n_second * m_n_third + i2 * m_n_third + i3];}

        size_t Total_Index(size_t i1, size_t i2, size_t i3) const{sb_assert(i1 < m_n_first && i2 < m_n_second && i3 < m_n_third && "Index out of range for Contiguous3D array"); return i1 * m_n_second * m_n_third + i2 * m_n_third + i3;}

        T& operator[](size_t total_index){return m_data[total_index];} // 
        
        T operator[](size_t total_index) const {return m_data[total_index];} // 

        size_t Number_of_First_Index () const {return m_n_first; }
        size_t Number_of_Second_Index() const {return m_n_second;}
        size_t Number_of_Third_Index () const {return m_n_third; } 

        const void* Buffer_Start()  const{return &m_data[0];}
        void* Modify_Buffer_Start() const{return &m_data[0];}

        void Write() const{
            std::cout<<" Contiguous3D at "<< this << " with shape ("<< this->Number_of_First_Index() <<", "<< this->Number_of_Second_Index()<< ", "<<this->Number_of_Third_Index()<< "):\n";
        }
        size_t m_first_stride;
        size_t m_second_stride;

    private:
        std::unique_ptr<T[]> m_data;
        size_t m_n_first; 
        size_t m_n_second; 
        size_t m_n_third; 
};


/**
 * @brief Contiguous 4D array
 * 
 * @tparam T 
 */
template <class T>
class Contiguous4D{
    public:
        Contiguous4D(size_t n_first, size_t n_second, size_t n_third, size_t n_fourth) : m_n_first(n_first), m_n_second(n_second), m_n_third(n_third), m_n_fourth(n_fourth), m_first_stride(n_second * n_third * n_fourth), m_second_stride(n_third * n_fourth), m_third_stride(n_fourth), m_data(std::make_unique<T[]>(n_first * n_second * n_third * n_fourth)){};

        T  operator()(size_t i1, size_t i2, size_t i3, size_t i4) const {
           sb_assert(i1 < m_n_first && i2 < m_n_second && i3 < m_n_third && i4 < m_n_fourth && "Index out of range for Contiguous4D array"); 
            return m_data[i1 * m_first_stride + i2 * m_second_stride +  i3 * m_n_fourth + i4];
        }
        T& operator()(size_t i1, size_t i2, size_t i3, size_t i4){
           sb_assert(i1 < m_n_first && i2 < m_n_second && i3 < m_n_third && i4 < m_n_fourth && "Index out of range for Contiguous4D array"); 
            return m_data[i1 * m_first_stride + i2 * m_second_stride + i3 * m_n_fourth + i4];
        }

        T& operator[](size_t total_index){return m_data[total_index];} // 
        size_t Number_of_First_Index () const {return m_n_first; }
        size_t Number_of_Second_Index() const {return m_n_second;}
        size_t Number_of_Third_Index () const {return m_n_third; } 
        size_t Number_of_Fourth_Index() const {return m_n_fourth;} 


        const void* Buffer_Start()  const{return &m_data[0];}
        void* Modify_Buffer_Start() const{return &m_data[0];}

        void Write() const{
            std::cout<<" Contiguous4D at "<< this << " with shape ("<< this->Number_of_First_Index() <<", "<< this->Number_of_Second_Index()<<","<<this->Number_of_Third_Index()<<","<<this->Number_of_Fourth_Index()<< "):\n";
        }
        void Set_Value(T val){
            for(size_t i=0; i < m_n_first * m_n_second * m_n_third * m_n_fourth; ++i){
                m_data[i] = val;
            }
        }
        size_t m_third_stride;
        size_t m_first_stride;
        size_t m_second_stride;

    private:
        std::unique_ptr<T[]> m_data;
        size_t m_n_first; 
        size_t m_n_second; 
        size_t m_n_third; 
        size_t m_n_fourth;
};