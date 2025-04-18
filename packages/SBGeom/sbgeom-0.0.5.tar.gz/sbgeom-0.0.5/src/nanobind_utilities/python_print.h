#pragma once
#include <nanobind/nanobind.h>
#include <nanobind/eigen/dense.h>
#include <string>
#include <nanobind/stl/shared_ptr.h>
#include <nanobind/stl/unique_ptr.h>
#include <nanobind/make_iterator.h>
#include <nanobind/stl/string.h>
#include <nanobind/eval.h>

#include "Post_Process.h"


class Python_Printer : public Printer{



    public: 
    Python_Printer(nanobind::object scope, unsigned verbosity) : m_scope(scope), m_verbosity(verbosity){};
    Python_Printer(nanobind::object scope) : m_scope(scope) {};
    void Print(std::string print_string, bool newline_end = true) const override{
        std::string aa;
        if(newline_end){
            aa = std::string("print(\'")+print_string+std::string("\', flush=True)");
        }
        else{
            aa = std::string("print(\'")+print_string+std::string("\', end='', flush=True)");
        }
        nanobind::exec(nanobind::str(aa.c_str()), m_scope);
    };
    unsigned Verbosity() const override{return m_verbosity;}
    
    private:
    unsigned m_verbosity = 10;
    nanobind::object m_scope;
};

class Python_Printer_Same_Line : public Printer{
    public: 
    Python_Printer_Same_Line(nanobind::object scope, unsigned verbosity) : m_scope(scope), m_verbosity(verbosity){};
    Python_Printer_Same_Line(nanobind::object scope) : m_scope(scope) {};
    void Print(std::string print_string, bool newline_end = true) const override{
        
        std::string aa = std::string("print(\'")+print_string+std::string("\', end='\\r', flush=True)");
        nanobind::exec(nanobind::str(aa.c_str()), m_scope);
    };
    unsigned Verbosity() const override{return m_verbosity;}

    private:
    unsigned m_verbosity = 10;
    nanobind::object m_scope;
};