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

#include "itktubeBasisFeatureVectorGenerator.h"
#include "itktubeBlurImageFunction.h"
#include "itktubeImageRegionMomentsCalculator.h"
#include "itktubeJointHistogramImageFunction.h"
#include "itktubeNJetFeatureVectorGenerator.h"
#include "itktubeNJetImageFunction.h"
#include "itktubeRidgeFeatureVectorGenerator.h"
#include "itktubeVectorImageToListGenerator.h"
#include "itktubeVotingResampleImageFunction.h"

#include <itkImage.h>

int tubeBaseNumericsPrintTest( int itkNotUsed( argc ), char * itkNotUsed( argv )[] )
{
  typedef itk::Image< float, 2 >                 ImageType;
  typedef itk::Image< itk::Vector<float, 2>, 2 > VectorImageType;

  itk::tube::ImageRegionMomentsCalculator< ImageType >::Pointer
    regionMomentsObject =
    itk::tube::ImageRegionMomentsCalculator< ImageType >::New();
  std::cout << "-------------itktubeImageRegionMomentsCalculator"
            << regionMomentsObject
            << std::endl;

  itk::tube::JointHistogramImageFunction< ImageType >::Pointer
    jointHistoObject =
    itk::tube::JointHistogramImageFunction< ImageType >::New();
  std::cout << "-------------itktubeJointHistogramImageFunction"
            << jointHistoObject
            << std::endl;

  itk::tube::BlurImageFunction< ImageType >::Pointer tbif =
    itk::tube::BlurImageFunction< ImageType > ::New();
  std::cout << "-------------tbif" << tbif << std::endl;

  itk::tube::NJetImageFunction< ImageType >::Pointer
    nJetObject =
    itk::tube::NJetImageFunction< ImageType >::New();
  std::cout << "-------------itktubeNJetImageFunction"
            << nJetObject
            << std::endl;

  itk::tube::NJetFeatureVectorGenerator< ImageType >::Pointer
    nJetFeatureVectorGenerator =
    itk::tube::NJetFeatureVectorGenerator< ImageType >::New();
  std::cout << "-------------NJetFeatureVectorGenerator"
    << nJetFeatureVectorGenerator << std::endl;

  itk::tube::BasisFeatureVectorGenerator< ImageType, ImageType >::Pointer
    basisFeatureVectorGenerator =
    itk::tube::BasisFeatureVectorGenerator< ImageType, ImageType >::New();
  std::cout << "-------------BasisFeatureVectorGenerator"
    << basisFeatureVectorGenerator << std::endl;

  itk::tube::RidgeFeatureVectorGenerator< ImageType >::Pointer
    ridgeFeatureVectorGenerator =
    itk::tube::RidgeFeatureVectorGenerator< ImageType >::New();
  std::cout << "-------------RidgeFeatureVectorGenerator"
    << ridgeFeatureVectorGenerator << std::endl;


  itk::tube::Statistics::VectorImageToListGenerator< VectorImageType,
      ImageType >::Pointer
    vectorImageToListObject =
    itk::tube::Statistics::VectorImageToListGenerator< VectorImageType,
      ImageType >::New();
  std::cout << "-------------itktubeVectorImageToListGenerator"
            << vectorImageToListObject
            << std::endl;

  itk::tube::VotingResampleImageFunction< ImageType >::Pointer
    votingResampleObject =
    itk::tube::VotingResampleImageFunction< ImageType >::New();
  std::cout << "-------------itktubeVotingResampleImageFunction"
            << votingResampleObject
            << std::endl;

  return EXIT_SUCCESS;
}
