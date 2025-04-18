#include "Node.h"

void print_tabs(unsigned number_of_tabs){
    for(unsigned i = 0 ; i < number_of_tabs; i++){
        std::cout<<"    ";
    };
};

void Node::Write() const{
    std::cout<<"Node at "<<this<<": [";
    printf("% .5f,",m_location[0]);
    printf("% .5f,",m_location[1]);
    printf("% .5f ",m_location[2]);
    std::cout<<"]"<<std::endl;
    
};

bool approx_float_sb(double d_1, double d_2){return fabs(d_1 - d_2) < 1e-4;}
