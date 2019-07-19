# Generated with SMOP  0.41
from libsmop import *
# /workspace/MOT/cmot-v1/ILDA/CJ_ilda07.m

    
@function
def CJ_ilda07(init_data=None,init_label=None,*args,**kwargs):
    varargin = CJ_ilda07.varargin
    nargin = CJ_ilda07.nargin

    #----------------
    # ILDA pseudocode
    # written by T-K. Kim, 2007
    dataset_1=copy(init_data)
# /workspace/MOT/cmot-v1/ILDA/CJ_ilda07.m:5
    label_1=copy(init_label)
# /workspace/MOT/cmot-v1/ILDA/CJ_ilda07.m:5
    
    numOfupdate=length(dataset_1)
# /workspace/MOT/cmot-v1/ILDA/CJ_ilda07.m:8
    eigenThreshold=1
# /workspace/MOT/cmot-v1/ILDA/CJ_ilda07.m:9
    for nupdate in arange(0,numOfupdate).reshape(-1):
        if (nupdate == 0):
            # init proc
            m_1,M_1,TeigenVect_1,TeigenVal_1=fGetStModel(dataset_1,eigenThreshold,nargout=4)
# /workspace/MOT/cmot-v1/ILDA/CJ_ilda07.m:14
            m_1,M_1,BeigenVect_1,BeigenVal_1,samplePerClass_1,meanPerClass_1=fGetSbModel(dataset_1,label_1,eigenThreshold,nargout=6)
# /workspace/MOT/cmot-v1/ILDA/CJ_ilda07.m:15
            DiscriminativeComponents,D=fGetDiscriminativeComponents(TeigenVect_1,TeigenVal_1,BeigenVect_1,BeigenVal_1,M_1,DeigenThreshold,nargout=2)
# /workspace/MOT/cmot-v1/ILDA/CJ_ilda07.m:16
        else:
            # for new data
            dataset_2=copy(New_data)
# /workspace/MOT/cmot-v1/ILDA/CJ_ilda07.m:19
            label_2=copy(New_label)
# /workspace/MOT/cmot-v1/ILDA/CJ_ilda07.m:19
            m_2,M_2,TeigenVect_2,TeigenVal_2=fGetStModel(dataset_2,eigenThreshold,nargout=4)
# /workspace/MOT/cmot-v1/ILDA/CJ_ilda07.m:20
            m_2,M_2,BeigenVect_2,BeigenVal_2,samplePerClass_2,meanPerClass_2=fGetSbModel(dataset_2,label_2,eigenThreshold,nargout=6)
# /workspace/MOT/cmot-v1/ILDA/CJ_ilda07.m:21
            outMean,outNSample,outEVect_t,outEVal_t=fMergeSt(m_1,M_1,TeigenVect_1,TeigenVal_1,m_2,M_2,TeigenVect_2,TeigenVal_2,eigenThreshold,nargout=4)
# /workspace/MOT/cmot-v1/ILDA/CJ_ilda07.m:24
            outMean,outNSample,outEVect_b,outEVal_b,outSamplePerClass,outMeanPerClass=fMergeSb(m_1,M_1,BeigenVect_1,BeigenVal_1,samplePerClass_1,meanPerClass_1,label_1,m_2,M_2,BeigenVect_2,BeigenVal_2,samplePerClass_2,meanPerClass_2,label_2,eigenThreshold,nargout=6)
# /workspace/MOT/cmot-v1/ILDA/CJ_ilda07.m:25
            DiscriminativeComponents,D=fGetDiscriminativeComponents(outEVect_t,outEVal_t,outEVect_b,outEVal_b,outNSample,DeigenThreshold,nargout=2)
# /workspace/MOT/cmot-v1/ILDA/CJ_ilda07.m:26
            m_1=copy(outMean)
# /workspace/MOT/cmot-v1/ILDA/CJ_ilda07.m:29
            M_1=copy(outNSample)
# /workspace/MOT/cmot-v1/ILDA/CJ_ilda07.m:29
            TeigenVect_1=copy(outEVect_t)
# /workspace/MOT/cmot-v1/ILDA/CJ_ilda07.m:29
            TeigenVal_1=copy(outEVal_t)
# /workspace/MOT/cmot-v1/ILDA/CJ_ilda07.m:29
            BeigenVect_1=copy(outEVect_b)
# /workspace/MOT/cmot-v1/ILDA/CJ_ilda07.m:30
            BeigenVal_1=copy(outEVal_b)
# /workspace/MOT/cmot-v1/ILDA/CJ_ilda07.m:30
            samplePerClass_1=copy(outSamplePerClass)
# /workspace/MOT/cmot-v1/ILDA/CJ_ilda07.m:31
            meanPerClass_1=copy(outMeanPerClass)
# /workspace/MOT/cmot-v1/ILDA/CJ_ilda07.m:31
            label_1=horzcat(label_1,label_2)
# /workspace/MOT/cmot-v1/ILDA/CJ_ilda07.m:32
    
    return m,n
    
if __name__ == '__main__':
    pass
    
