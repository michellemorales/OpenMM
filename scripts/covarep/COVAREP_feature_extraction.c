/*
 * MATLAB Compiler: 6.4 (R2017a)
 * Date: Fri Mar 24 09:57:47 2017
 * Arguments: "-B""macro_default""-l""COVAREP_feature_extraction.m"
 */

#include <stdio.h>
#define EXPORTING_COVAREP_feature_extraction 1
#include "COVAREP_feature_extraction.h"

static HMCRINSTANCE _mcr_inst = NULL;


#ifdef __cplusplus
extern "C" {
#endif

static int mclDefaultPrintHandler(const char *s)
{
  return mclWrite(1 /* stdout */, s, sizeof(char)*strlen(s));
}

#ifdef __cplusplus
} /* End extern "C" block */
#endif

#ifdef __cplusplus
extern "C" {
#endif

static int mclDefaultErrorHandler(const char *s)
{
  int written = 0;
  size_t len = 0;
  len = strlen(s);
  written = mclWrite(2 /* stderr */, s, sizeof(char)*len);
  if (len > 0 && s[ len-1 ] != '\n')
    written += mclWrite(2 /* stderr */, "\n", sizeof(char));
  return written;
}

#ifdef __cplusplus
} /* End extern "C" block */
#endif

/* This symbol is defined in shared libraries. Define it here
 * (to nothing) in case this isn't a shared library. 
 */
#ifndef LIB_COVAREP_feature_extraction_C_API
#define LIB_COVAREP_feature_extraction_C_API /* No special import/export declaration */
#endif

LIB_COVAREP_feature_extraction_C_API 
bool MW_CALL_CONV COVAREP_feature_extractionInitializeWithHandlers(
    mclOutputHandlerFcn error_handler,
    mclOutputHandlerFcn print_handler)
{
    int bResult = 0;
  if (_mcr_inst != NULL)
    return true;
  if (!mclmcrInitialize())
    return false;
    {
        mclCtfStream ctfStream = 
            mclGetEmbeddedCtfStream((void 
                                                     *)(COVAREP_feature_extractionInitializeWithHandlers));
        if (ctfStream) {
            bResult = mclInitializeComponentInstanceEmbedded(   &_mcr_inst,
                                                                error_handler, 
                                                                print_handler,
                                                                ctfStream);
            mclDestroyStream(ctfStream);
        } else {
            bResult = 0;
        }
    }  
    if (!bResult)
    return false;
  return true;
}

LIB_COVAREP_feature_extraction_C_API 
bool MW_CALL_CONV COVAREP_feature_extractionInitialize(void)
{
  return COVAREP_feature_extractionInitializeWithHandlers(mclDefaultErrorHandler, 
                                                          mclDefaultPrintHandler);
}

LIB_COVAREP_feature_extraction_C_API 
void MW_CALL_CONV COVAREP_feature_extractionTerminate(void)
{
  if (_mcr_inst != NULL)
    mclTerminateInstance(&_mcr_inst);
}

LIB_COVAREP_feature_extraction_C_API 
void MW_CALL_CONV COVAREP_feature_extractionPrintStackTrace(void) 
{
  char** stackTrace;
  int stackDepth = mclGetStackTrace(&stackTrace);
  int i;
  for(i=0; i<stackDepth; i++)
  {
    mclWrite(2 /* stderr */, stackTrace[i], sizeof(char)*strlen(stackTrace[i]));
    mclWrite(2 /* stderr */, "\n", sizeof(char)*strlen("\n"));
  }
  mclFreeStackTrace(&stackTrace, stackDepth);
}


LIB_COVAREP_feature_extraction_C_API 
bool MW_CALL_CONV mlxCOVAREP_feature_extraction(int nlhs, mxArray *plhs[], int nrhs, 
                                                mxArray *prhs[])
{
  return mclFeval(_mcr_inst, "COVAREP_feature_extraction", nlhs, plhs, nrhs, prhs);
}

LIB_COVAREP_feature_extraction_C_API 
bool MW_CALL_CONV mlfCOVAREP_feature_extraction(mxArray* in_dir, mxArray* sample_rate)
{
  return mclMlfFeval(_mcr_inst, "COVAREP_feature_extraction", 0, 0, 2, in_dir, sample_rate);
}

