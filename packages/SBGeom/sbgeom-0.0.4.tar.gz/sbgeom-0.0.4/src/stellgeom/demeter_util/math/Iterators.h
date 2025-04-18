#pragma once
#include <iterator>

/**
 * @brief Simple iterator over a vector member
 * 
 * Can lead to very simple code for loops like 
 * \code 
 * for(auto& i : quadrature_set){ 
 * ....
 * }
 * \endcode
 * 
 * Usage: e.g. in a Quadrature_Set:
 * 
 * \code
 * using iterator = Vector_Iterator<Direction>;
 *  iterator begin() const { return iterator(&(*m_direction_vectors.begin())); };
 *  iterator end() const { return iterator(&(*m_direction_vectors.end())); };
 *\endcode
 * 
 * @tparam data_class iterator class
 */
template<class data_class>
class Vector_Iterator{

    public: 
        using value_type =const data_class;
        using difference_type = std::ptrdiff_t;
        using pointer =const data_class*;
        using reference = const data_class&;
        using iterator_category = std::bidirectional_iterator_tag;
        Vector_Iterator(pointer ptr) : m_ptr(ptr){}        

        reference operator*() const{return *m_ptr;}
        pointer operator->() const{return m_ptr;}
        Vector_Iterator& operator++(){m_ptr++; return *this;}
        Vector_Iterator operator++(int){Vector_Iterator tmp = *this; ++(*this); return tmp;}

        Vector_Iterator& operator--(){m_ptr--; return *this;}
        Vector_Iterator operator--(int){Vector_Iterator tmp = *this; --(*this); return tmp;}

        bool operator==(const Vector_Iterator& other){ return this->m_ptr == other.m_ptr;}
        bool operator!=(const Vector_Iterator& other){ return this->m_ptr != other.m_ptr;}


    private:

        pointer m_ptr;
};