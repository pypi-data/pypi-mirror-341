#include <iostream>
#include "sstream"
/// ASSERT(condition) checks if the condition is met, and if not, calls
/// ABORT with an error message indicating the module and line where
/// the error occurred. 
// These are only for development and should only be used for things that the user cannot make happen.
#ifdef CHECK_ASSERT_DEBUG
#define sb_assert(x)                                                                \
    if (!(x)) {                                                                     \
        std::stringstream ss;                                                       \
        ss<< "Assertion failed in"<<__FILE__<<", line"<<__LINE__<<std::endl;        \
        throw std::runtime_error(ss.str());                                         \
    }                                                                               \
    else   // This 'else' exists to catch the user's following semicolon
#else
#define sb_assert(x) /*nothing*/
#endif

#ifdef CHECK_ASSERT_SB // Checks and outputs a message. Also couts the message to make it usable in OMP regions.
#define sb_assert_message(x, message)                                               \
    if (!(x)) {                                                                     \
        std::cerr<<message<<'\n';                                                   \
        throw std::runtime_error(message);                                          \
    }                                                                               \
    else   // This 'else' exists to catch the user's following semicolon
#else
#define sb_assert_message(x, message) /*nothing*/
#endif


