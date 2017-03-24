/*
 * MATLAB Compiler: 6.4 (R2017a)
 * Date: Fri Mar 24 09:57:47 2017
 * Arguments: "-B""macro_default""-l""COVAREP_feature_extraction.m"
 */

#ifndef __COVAREP_feature_extraction_h
#define __COVAREP_feature_extraction_h 1

#if defined(__cplusplus) && !defined(mclmcrrt_h) && defined(__linux__)
#  pragma implementation "mclmcrrt.h"
#endif
#include "mclmcrrt.h"
#ifdef __cplusplus
extern "C" {
#endif

#if defined(__SUNPRO_CC)
/* Solaris shared libraries use __global, rather than mapfiles
 * to define the API exported from a shared library. __global is
 * only necessary when building the library -- files including
 * this header file to use the library do not need the __global
 * declaration; hence the EXPORTING_<library> logic.
 */

#ifdef EXPORTING_COVAREP_feature_extraction
#define PUBLIC_COVAREP_feature_extraction_C_API __global
#else
#define PUBLIC_COVAREP_feature_extraction_C_API /* No import statement needed. */
#endif

#define LIB_COVAREP_feature_extraction_C_API PUBLIC_COVAREP_feature_extraction_C_API

#elif defined(_HPUX_SOURCE)

#ifdef EXPORTING_COVAREP_feature_extraction
#define PUBLIC_COVAREP_feature_extraction_C_API __declspec(dllexport)
#else
#define PUBLIC_COVAREP_feature_extraction_C_API __declspec(dllimport)
#endif

#define LIB_COVAREP_feature_extraction_C_API PUBLIC_COVAREP_feature_extraction_C_API


#else

#define LIB_COVAREP_feature_extraction_C_API

#endif

/* This symbol is defined in shared libraries. Define it here
 * (to nothing) in case this isn't a shared library. 
 */
#ifndef LIB_COVAREP_feature_extraction_C_API 
#define LIB_COVAREP_feature_extraction_C_API /* No special import/export declaration */
#endif

extern LIB_COVAREP_feature_extraction_C_API 
bool MW_CALL_CONV COVAREP_feature_extractionInitializeWithHandlers(
       mclOutputHandlerFcn error_handler, 
       mclOutputHandlerFcn print_handler);

extern LIB_COVAREP_feature_extraction_C_API 
bool MW_CALL_CONV COVAREP_feature_extractionInitialize(void);

extern LIB_COVAREP_feature_extraction_C_API 
void MW_CALL_CONV COVAREP_feature_extractionTerminate(void);



extern LIB_COVAREP_feature_extraction_C_API 
void MW_CALL_CONV COVAREP_feature_extractionPrintStackTrace(void);

extern LIB_COVAREP_feature_extraction_C_API 
bool MW_CALL_CONV mlxCOVAREP_feature_extraction(int nlhs, mxArray *plhs[], int nrhs, 
                                                mxArray *prhs[]);



extern LIB_COVAREP_feature_extraction_C_API bool MW_CALL_CONV mlfCOVAREP_feature_extraction(mxArray* in_dir, mxArray* sample_rate);

#ifdef __cplusplus
}
#endif
#endif
