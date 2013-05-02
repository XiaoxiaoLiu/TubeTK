/*=========================================================================

Library:   TubeTK

Copyright 2010 Kitware Inc. 28 Corporate Drive,
Clifton Park, NY, 12065, USA.

All rights reserved.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

=========================================================================*/

#ifndef __itkSpatialObjectSource_txx
#define __itkSpatialObjectSource_txx

#include "itkSpatialObjectSource.h"

namespace itk
{

template< class TOutputSpatialObject >
SpatialObjectSource< TOutputSpatialObject >
::SpatialObjectSource( void )
{
  // Create the output. We use static_cast<> here because we know the default
  // output must be of type TOutputSpatialObject
  typename TOutputSpatialObject::Pointer output =
    static_cast< TOutputSpatialObject * >( this->MakeOutput(0).GetPointer() );
  this->ProcessObject::SetNumberOfRequiredOutputs(1);
  this->ProcessObject::SetNthOutput( 0, output.GetPointer() );
}


template< class TOutputSpatialObject >
ProcessObject::DataObjectPointer
SpatialObjectSource< TOutputSpatialObject >
::MakeOutput( ProcessObject::DataObjectPointerArraySizeType itkNotUsed(idx) )
{
  return OutputSpatialObjectType::New().GetPointer();
}


template< class TOutputSpatialObject >
typename SpatialObjectSource< TOutputSpatialObject >::OutputSpatialObjectType *
SpatialObjectSource< TOutputSpatialObject >
::GetOutput( void )
{
  // we assume that the first output is of the templated type
  return itkDynamicCastInDebugMode< TOutputSpatialObject * >
    ( this->GetPrimaryOutput() );
}


template< class TOutputSpatialObject >
const typename SpatialObjectSource< TOutputSpatialObject >::OutputSpatialObjectType *
SpatialObjectSource< TOutputSpatialObject >
::GetOutput( void ) const
{
  // we assume that the first output is of the templated type
  return itkDynamicCastInDebugMode< const TOutputSpatialObject * >
    ( this->GetPrimaryOutput() );
}


template< class TOutputSpatialObject >
typename SpatialObjectSource< TOutputSpatialObject >::OutputSpatialObjectType *
SpatialObjectSource< TOutputSpatialObject >
::GetOutput( unsigned int idx )
{
  OutputSpatialObjectType * output = dynamic_cast< OutputSpatialObjectType * >
                      ( this->ProcessObject::GetOutput(idx) );

  if( output == NULL && this->ProcessObject::GetOutput(idx) != NULL )
    {
    itkWarningMacro (<< "Unable to convert output number " << idx
      << " to type " <<  typeid( OutputSpatialObjectType ).name() );
    }
  return output;
}


template< class TOutputSpatialObject >
void
SpatialObjectSource< TOutputSpatialObject >
::GraftOutput(DataObject *graft)
{
  this->GraftNthOutput(0, graft);
}


template< class TOutputSpatialObject >
void
SpatialObjectSource< TOutputSpatialObject >
::GraftOutput(const DataObjectIdentifierType & key, DataObject *graft)
{
  if( !graft )
    {
    itkExceptionMacro(<< "Requested to graft output that is a NULL pointer");
    }

  // we use the process object method since all out output may not be
  // of the same type
  DataObject *output = this->ProcessObject::GetOutput(key);

  // Call GraftImage to copy meta-information, regions, and the pixel container
  output->Graft(graft);
}


template< class TOutputSpatialObject >
void
SpatialObjectSource< TOutputSpatialObject >
::GraftNthOutput(unsigned int idx, DataObject *graft)
{
  if( idx >= this->GetNumberOfIndexedOutputs() )
    {
    itkExceptionMacro(<< "Requested to graft output " << idx
                      << " but this filter only has " << this->GetNumberOfIndexedOutputs() << " indexed Outputs.");
    }
  this->GraftOutput( this->MakeNameFromOutputIndex(idx), graft );
}

} // End namespace itk

#endif // End !defined(__itkSpatialObjectSource_txx)
