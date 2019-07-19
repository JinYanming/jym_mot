# Generated with SMOP  0.41
from libsmop import *
# ../munkres.m

    
@function
def munkres(costMat=None,*args,**kwargs):
    varargin = munkres.varargin
    nargin = munkres.nargin

    # MUNKRES   Munkres Assign Algorithm
    
    # [ASSIGN,COST] = munkres(COSTMAT) returns the optimal assignment in ASSIGN
# with the minimum COST based on the assignment problem represented by the
# COSTMAT, where the (i,j)th element represents the cost to assign the jth
# job to the ith worker.
    
    # This is vectorized implementation of the algorithm. It is the fastest
# among all Matlab implementations of the algorithm.
    
    # Examples
# Example 1: a 5 x 5 example
#{
    assignment,cost=munkres(magic(5),nargout=2)
    assignedrows,dum=find(assignment,nargout=2)
    disp(assignedrows.T)
    
    disp(cost)
    
    #}
# Example 2: 400 x 400 random data
#{
    n=400
    A=rand(n)
    tic
    a,b=munkres(A,nargout=2)
    toc
    #}
    
    # Reference:
# "Munkres' Assignment Algorithm, Modified for Rectangular Matrices", 
# http://csclab.murraystate.edu/bob.pilgrim/445/munkres.html
    
    # version 1.0 by Yi Cao at Cranfield University on 17th June 2008
    
    assignment=false(size(costMat))
    cost=0
    costMat[costMat != costMat]=Inf
    validMat=costMat < Inf
    validCol=any(validMat)
    validRow=any(validMat,2)
    nRows=sum(validRow)
    nCols=sum(validCol)
    n=max(nRows,nCols)
    if logical_not(n):
        return assignment,cost
    
    
    dMat=zeros(n)
    dMat[arange(1,nRows),arange(1,nCols)]=costMat(validRow,validCol)
    #*************************************************
# Munkres' Assignment Algorithm starts here
#*************************************************
    
    #########################################################
#   STEP 1: Subtract the row minimum from each row.
#########################################################
    dMat=bsxfun(minus,dMat,min(dMat,[],2))
    #**************************************************************************  
#   STEP 2: Find a zero of dMat. If there are no starred zeros in its
#           column or row start the zero. Repeat for each zero
#**************************************************************************
    zP=logical_not(dMat)
    starZ=false(n)
    while any(ravel(zP)):

        r,c=find(zP,1,nargout=2)
        starZ[r,c]=true
        zP[r,arange()]=false
        zP[arange(),c]=false

    
    while 1:

        #**************************************************************************
#   STEP 3: Cover each column with a starred zero. If all the columns are
#           covered then the matching is maximum
#**************************************************************************
        primeZ=false(n)
        coverColumn=any(starZ)
        if logical_not(any(logical_not(coverColumn))):
            break
        coverRow=false(n,1)
        while 1:

            #**************************************************************************
        #   STEP 4: Find a noncovered zero and prime it.  If there is no starred
        #           zero in the row containing this primed zero, Go to Step 5.  
        #           Otherwise, cover this row and uncover the column containing 
        #           the starred zero. Continue in this manner until there are no 
        #           uncovered zeros left. Save the smallest uncovered value and 
        #           Go to Step 6.
        #**************************************************************************
            ravel[zP]=false
            zP[logical_not(coverRow),logical_not(coverColumn)]=logical_not(dMat(logical_not(coverRow),logical_not(coverColumn)))
            Step=6
            while any(any(zP(logical_not(coverRow),logical_not(coverColumn)))):

                uZr,uZc=find(zP,1,nargout=2)
                primeZ[uZr,uZc]=true
                stz=starZ(uZr,arange())
                if logical_not(any(stz)):
                    Step=5
                    break
                coverRow[uZr]=true
                coverColumn[stz]=false
                zP[uZr,arange()]=false
                zP[logical_not(coverRow),stz]=logical_not(dMat(logical_not(coverRow),stz))

            if Step == 6:
                # *************************************************************************
            # STEP 6: Add the minimum uncovered value to every element of each covered
            #         row, and subtract it from every element of each uncovered column.
            #         Return to Step 4 without altering any stars, primes, or covered lines.
            #**************************************************************************
                M=dMat(logical_not(coverRow),logical_not(coverColumn))
                minval=min(min(M))
                if minval == inf:
                    return assignment,cost
                dMat[coverRow,coverColumn]=dMat(coverRow,coverColumn) + minval
                dMat[logical_not(coverRow),logical_not(coverColumn)]=M - minval
            else:
                break

        #**************************************************************************
    # STEP 5:
    #  Construct a series of alternating primed and starred zeros as
    #  follows:
    #  Let Z0 represent the uncovered primed zero found in Step 4.
    #  Let Z1 denote the starred zero in the column of Z0 (if any).
    #  Let Z2 denote the primed zero in the row of Z1 (there will always
    #  be one).  Continue until the series terminates at a primed zero
    #  that has no starred zero in its column.  Unstar each starred
    #  zero of the series, star each primed zero of the series, erase
    #  all primes and uncover every line in the matrix.  Return to Step 3.
    #**************************************************************************
        rowZ1=starZ(arange(),uZc)
        starZ[uZr,uZc]=true
        while any(rowZ1):

            starZ[rowZ1,uZc]=false
            uZc=primeZ(rowZ1,arange())
            uZr=copy(rowZ1)
            rowZ1=starZ(arange(),uZc)
            starZ[uZr,uZc]=true


    
    # Cost of assignment
    assignment[validRow,validCol]=starZ(arange(1,nRows),arange(1,nCols))
    cost=sum(costMat(assignment))
