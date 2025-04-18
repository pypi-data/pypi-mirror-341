#pragma once
#include <iostream>


#ifdef _OPENMP
    #include <omp.h>
#else
    #define omp_get_thread_num() 0 
    #define omp_get_num_threads() 1
    #define omp_get_max_threads() 1
#endif

class Progress_Task {
    public:
        Progress_Task(unsigned total_iterations) : m_total_iterations(total_iterations / omp_get_max_threads()), m_percent_number(0){};
 
        void Update_Output(unsigned iteration){
            if(omp_get_thread_num() == 0){
                if(double(iteration*100)/double(m_total_iterations) > double(m_percent_number)){
                    std::cerr<<'\r'<<m_percent_number<< "%";
                    m_percent_number = unsigned(double(iteration*100)/double(m_total_iterations));
                }
            }
        };
        ~Progress_Task(){std::cerr<<'\r'<<"    "<<'\n'<<std::endl;;}
    private:
        unsigned m_percent_number;
        unsigned m_total_iterations;
};