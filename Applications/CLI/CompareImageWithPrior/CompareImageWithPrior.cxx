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

#if defined(_MSC_VER)
#pragma warning ( disable : 4786 )
#endif

#ifdef __BORLANDC__
#define ITK_LEAN_AND_MEAN
#endif

// It is important to use OrientedImages
#include "itkOrientedImage.h"
#include "itkImageFileReader.h"
#include "itkImageFileWriter.h"
#include "itkImageRegionConstIteratorWithIndex.h"
#include "itkAddImageFilter.h"
#include "itkSubtractImageFilter.h"
#include "itkSquareImageFilter.h"
#include "itkSqrtImageFilter.h"
#include "itkDivideByConstantImageFilter.h"
#include "itkMultiplyByConstantImageFilter.h"
#include "itkMinimumMaximumImageCalculator.h"
#include "vnl/vnl_math.h"

// The following three should be used in every CLI application
#include "tubeCLIFilterWatcher.h"
#include "tubeCLIProgressReporter.h"
#include "itkTimeProbesCollectorBase.h"

// Local Includes for helper functions
#include "tubeSubImageGenerator.h"
#include "tubeJointHistogramGenerator.h"

// Includes specific to this CLI application
#include "itkRecursiveGaussianImageFilter.h"

// Must do a forward declaraction of DoIt before including
// tubeCLIHelperFunctions
template< class pixelT, unsigned int dimensionT >
int DoIt( int argc, char * argv[] );

// Must include CLP before including tubeCLIHleperFunctions
#include "CompareImageWithPriorCLP.h"

// Includes tube::ParseArgsAndCallDoIt function
#include "tubeCLIHelperFunctions.h"

// Your code should be within the DoIt function...
template< class pixelT, unsigned int dimensionT >
int DoIt( int argc, char * argv[] )
{
  PARSE_ARGS;

  // The timeCollector is used to perform basic profiling of the components
  //   of your algorithm.
  itk::TimeProbesCollectorBase timeCollector;

  // CLIProgressReporter is used to communicate progress with the Slicer GUI
  tube::CLIProgressReporter    progressReporter( "CompareImageWithPrior",
                                                 CLPProcessInformation );
  progressReporter.Start();

  // typedefs for inputs
  typedef float                                              PixelType;
  typedef itk::Image< PixelType,  dimensionT >               ImageType;
  typedef itk::ImageFileReader< ImageType >                  ReaderType;
  typedef itk::ImageFileWriter< ImageType  >                 WriterType;

  // typedefs for internal storage
  typedef std::vector<int>                                   VectorType;
  typedef typename tube::JointHistogramGenerator<PixelType,dimensionT>
    ::JointHistogramType                                     HistogramType;
  typedef itk::ImageFileReader< HistogramType >              HistReaderType;
  typedef itk::ImageFileWriter< HistogramType>               HistWriterType;

  // typedefs for iterators
  typedef itk::ImageRegionConstIteratorWithIndex<ImageType > FullItrType;
  typedef itk::ImageRegionConstIterator<HistogramType>       HistIteratorType;

  // typedefs for mathematical filters
  typedef itk::DivideByConstantImageFilter< HistogramType, double,
    HistogramType >                                          DividerType;
  typedef itk::MultiplyByConstantImageFilter< HistogramType, double,
    HistogramType >                                          MultiplierType;
  typedef itk::AddImageFilter< HistogramType, HistogramType, HistogramType>
                                                             AdderType;
  typedef itk::SubtractImageFilter< HistogramType, HistogramType,
    HistogramType>                                           SubtracterType;
  typedef itk::SquareImageFilter< HistogramType, HistogramType >
                                                             SquareType;
  typedef itk::SqrtImageFilter< HistogramType, HistogramType >
                                                             SqrtType;
  typedef itk::MinimumMaximumImageCalculator<ImageType>      CalculatorType;

  // Setup the readers to load the input data (image + prior)
  timeCollector.Start("Load data");
  typename ReaderType::Pointer reader = ReaderType::New();
  typename ReaderType::Pointer priorReader = ReaderType::New();
  reader->SetFileName( inputVolume.c_str() );
  priorReader->SetFileName( priorVolume.c_str() );

  // Load the input image with exception handling
  try
    {
    reader->Update();
    }
  catch( itk::ExceptionObject & err )
    {
    std::cerr << "ExceptionObject caught while reading the input image!"
              << std::endl;
    std::cerr << err << std::endl;
    return EXIT_FAILURE;
    }

  // Load the input prior with exception handling
  try
    {
    priorReader->Update();
    }
  catch( itk::ExceptionObject & err )
    {
    std::cerr << "ExceptionObject caught while reading the input prior!"
              << std::endl;
    std::cerr << err << std::endl;
    return EXIT_FAILURE;
    }
  timeCollector.Stop("Load data");
  double progress = 0.1;
  progressReporter.Report( progress );

  // Store the input images and prepare the target regions
  typename ImageType::Pointer curImage = reader->GetOutput();
  typename ImageType::Pointer curPrior = priorReader->GetOutput();
  typename ImageType::RegionType region;
  typename ImageType::RegionType fullRegion;
  typename ImageType::SizeType size;
  typename ImageType::IndexType start;
  VectorType roiSize(dimensionT);

  // Setup the target regions
  size = curImage->GetLargestPossibleRegion().GetSize();
  start = curImage->GetLargestPossibleRegion().GetIndex();
  for( unsigned int i = 0; i < dimensionT; ++i )
    {
    size[i] -= regionRadius;
    start[i] += regionRadius/2;
    roiSize[i] = regionRadius;
    }
  region.SetSize(size);
  region.SetIndex(start);

  // Allocate the output image and fill with 0s
  typename ImageType::Pointer outImage = ImageType::New();
  outImage->SetRegions(curImage->GetLargestPossibleRegion());
  outImage->Allocate();
  outImage->FillBuffer(0);

  FullItrType imageItr( curImage, region);

  // The first iteration through the image is to get the number of samples that
  // we will use in the other iterations. This allows for the super-granular
  // progress reporting that we all know and love.
  imageItr.GoToBegin();
  typename HistogramType::PixelType samples = 0;
  while( !imageItr.IsAtEnd() )
    {
    bool doCalculation = true;
    bool useThreshold;
    bool useSkip;
    if( threshold != 0 )
      {
      useThreshold = true;
      useSkip = false;
      }
    else if( skipSize != -1 )
      {
      useThreshold = false;
      useSkip = true;
      }
    else
      {
      useThreshold = false;
      useSkip = false;
      }

    if( useThreshold && imageItr.Get() > threshold )
      {
      doCalculation = false;
      }

    typename ImageType::IndexType curIndex;
    std::vector<int> roiCenter;
    if( doCalculation )
      {
      curIndex = imageItr.GetIndex();
      roiCenter = std::vector<int>(dimensionT);
      for( unsigned int i = 0; i < dimensionT; ++i )
        {
        if( useSkip && (curIndex[i]-start[i]) % skipSize != 0 )
          {
          doCalculation = false;
          break;
          }
        roiCenter[i] = curIndex[i];
        }
      }

    if( doCalculation )
      {
      ++samples;
      }
    ++imageItr;
    }

  // Caculate Image and Mask's Max and Min
  typename ImageType::PixelType imageMin;
  typename ImageType::PixelType imageMax;
  typename ImageType::PixelType maskMin;
  typename ImageType::PixelType maskMax;
  typename CalculatorType::Pointer calculator;
  calculator = CalculatorType::New();
  calculator->SetImage(curImage);
  calculator->Compute();
  imageMin = calculator->GetMinimum();
  imageMax = calculator->GetMaximum();
  calculator = CalculatorType::New();
  calculator->SetImage(curPrior);
  calculator->Compute();
  maskMin = calculator->GetMinimum();
  maskMax = calculator->GetMaximum();

  // Get some memory ready for our joint histograms
  typename HistogramType::Pointer hist;
  typename HistogramType::Pointer sumHist;
  typename HistogramType::Pointer sumSqrHist;
  typename HistogramType::Pointer meanHist;
  typename HistogramType::Pointer stdevHist;

  // variable for managing the granularity of progress reporting. The loop uses
  // progress += proportion/samples to appropriately gauge progress.
  double proportion;

  // If we've specified mean and stdev inputs, load them and don't do the
  // computation.
  if( mean != std::string("nil") && stdev != std::string("nil") )
    {
    timeCollector.Start("Load Mean and Stdev");

    // Setup reader for mean histogram
    typename HistReaderType::Pointer histReader;
    histReader = HistReaderType::New();
    histReader->SetFileName(mean);

    // Read mean histogram with exception handling
    try
      {
      histReader->Update();
      }
    catch( itk::ExceptionObject & err )
      {
      std::cerr << "ExceptionObject caught while reading the mean histogram!"
                << std::endl;
      std::cerr << err << std::endl;
      return EXIT_FAILURE;
      }
    meanHist = histReader->GetOutput();

    // Setup reader for standard deviation histogram
    histReader = HistReaderType::New();
    histReader->SetFileName(stdev);

    // Read standard deviation histogram with exception handling
    try
      {
      histReader->Update();
      }
    catch( itk::ExceptionObject & err )
      {
      std::cerr << "ExceptionObject caught while reading the stdev histogram!"
                << std::endl;
      std::cerr << err << std::endl;
      return EXIT_FAILURE;
      }
    stdevHist = histReader->GetOutput();

    proportion = 0.75;

    timeCollector.Stop("Load Mean and Stdev");
    }
  // If no mean and stdev inputs are specified we'll calculate them
  else
    {

    // Calculate the mean and standard deviation histograms
    timeCollector.Start("Get Mean and Stdev");
    bool firstPass = true;
    proportion = 0.40;
    imageItr.GoToBegin();
    while( !imageItr.IsAtEnd() )
      {
      bool doCalculation = true;
      bool useThreshold;
      bool useSkip;
      if( threshold != 0 )
        {
        useThreshold = true;
        useSkip = false;
        }
      else if( skipSize != -1 )
        {
        useThreshold = false;
        useSkip = true;
        }
      else
        {
        useThreshold = false;
        useSkip = false;
        }

      if( useThreshold && imageItr.Get() > threshold )
        {
        doCalculation = false;
        }

      typename ImageType::IndexType curIndex;
      std::vector<int> roiCenter;
      if( doCalculation )
        {
        curIndex = imageItr.GetIndex();
        roiCenter = std::vector<int>(dimensionT);
        for( unsigned int i = 0; i < dimensionT; ++i )
          {
          if( useSkip && (curIndex[i]-start[i]) % skipSize != 0 )
            {
            doCalculation = false;
            break;
            }
          roiCenter[i] = curIndex[i];
          }
        }

      if( doCalculation )
        {
        tube::SubImageGenerator<PixelType,dimensionT> subGenerator;
        subGenerator.SetRoiCenter(roiCenter);
        subGenerator.SetRoiSize(roiSize);
        subGenerator.SetInputVolume(curImage);
        subGenerator.SetInputMask(curPrior);
        subGenerator.Update();

        tube::JointHistogramGenerator<PixelType,dimensionT> histGenerator;
        histGenerator.SetInputVolume(subGenerator.GetOutputVolume());
        histGenerator.SetInputMask(subGenerator.GetOutputMask());
        histGenerator.SetNumberOfBins(histogramSize);
        histGenerator.SetInputMin(imageMin);
        histGenerator.SetInputMax(imageMax);
        histGenerator.SetMaskMin(maskMin);
        histGenerator.SetMaskMax(maskMax);
        histGenerator.Update();
        hist = histGenerator.GetOutputVolume();

        if( firstPass )
          {
          typename HistogramType::RegionType histRegion =
            hist->GetLargestPossibleRegion();
          sumHist = HistogramType::New();
          sumHist->SetRegions(histRegion);
          sumHist->Allocate();
          sumHist->FillBuffer(0);
          sumSqrHist = HistogramType::New();
          sumSqrHist->SetRegions(histRegion);
          sumSqrHist->Allocate();
          sumSqrHist->FillBuffer(0);
          firstPass = false;
          }

        typename AdderType::Pointer adder = AdderType::New();
        typename SquareType::Pointer square = SquareType::New();

        // Calculate Running Sum
        adder->SetInput1(sumHist);
        adder->SetInput2(hist);
        adder->Update();
        sumHist = adder->GetOutput();

        // Calculate Running Sum of Squares
        adder = AdderType::New();
        square->SetInput(hist);
        square->Update();
        adder->SetInput1(sumSqrHist);
        adder->SetInput2(square->GetOutput());
        adder->Update();
        sumSqrHist = adder->GetOutput();

        progress += proportion/samples;
        progressReporter.Report( progress );
        }
      ++imageItr;
      }
    timeCollector.Stop("Get Mean and Stdev");

    // Calculate the mean
    timeCollector.Start("Calculate Mean and Stdev");
    typename DividerType::Pointer divider = DividerType::New();
    divider->SetInput( sumHist );
    divider->SetConstant( samples );
    divider->Update();
    meanHist = divider->GetOutput();

    // Calculate the standard deviation
    typename SubtracterType::Pointer subtracter = SubtracterType::New();
    typename SquareType::Pointer square = SquareType::New();
    typename MultiplierType::Pointer multiplier = MultiplierType::New();
    typename SqrtType::Pointer sqrt = SqrtType::New();
    divider = DividerType::New();
    typename HistogramType::Pointer meanSquaredDivided;
    typename HistogramType::Pointer sumSquaresDivided;
    typename HistogramType::PixelType meanCo = samples/(samples-1);
    square->SetInput(meanHist);
    square->Update();
    multiplier->SetInput(square->GetOutput());
    multiplier->SetConstant( meanCo );
    multiplier->Update();
    meanSquaredDivided = multiplier->GetOutput();
    divider->SetInput(sumSqrHist);
    divider->SetConstant(samples-1);
    divider->Update();
    sumSquaresDivided = divider->GetOutput();
    subtracter->SetInput1(sumSquaresDivided);
    subtracter->SetInput2(meanSquaredDivided);
    subtracter->Update();
    sqrt->SetInput(subtracter->GetOutput());
    sqrt->Update();
    stdevHist = sqrt->GetOutput();

    timeCollector.Stop("Calculate Mean and Stdev");

    proportion = 0.35;
    }

  // Write the mean and standard deviation histograms to disk
  timeCollector.Start("Write Mean and Stdev");

  // Setup the mean histogram writer
  typename HistWriterType::Pointer histWriter = HistWriterType::New();
  histWriter->SetFileName( meanOutput.c_str() );
  histWriter->SetInput(meanHist);

  // Write the mean histogram to disk, with exception handling
  try
    {
    histWriter->Update();
    }
  catch( itk::ExceptionObject & err )
    {
    std::cerr << "ExceptionObject caught while writing the mean histogram!"
              << std::endl;
    std::cerr << err << std::endl;
    }

  // Setup the standard deviation histogram writer
  typename HistWriterType::Pointer stdWriter = HistWriterType::New();
  stdWriter->SetFileName( stdevOutput.c_str() );
  stdWriter->SetInput(stdevHist);

  // Write the stdev histogram to disk, with exception handling
  try
    {
    stdWriter->Update();
    }
  catch( itk::ExceptionObject & err )
    {
    std::cerr << "ExceptionObject caught while writing the stdev histogram!"
              << std::endl;
    std::cerr << err << std::endl;
    }
  timeCollector.Stop("Write Mean and Stdev");

  // Report progress after the mean and stdev write
  progress += 0.05;
  progressReporter.Report( progress );

  // Iterate through the image for a third and final time to calculate the Z
  // scores in the manner specified.
  timeCollector.Start("Calculate Z Scores");
  imageItr.GoToBegin();
  while( !imageItr.IsAtEnd() )
    {
    bool doCalculation = true;
    bool useThreshold;
    bool useSkip;
    if( threshold != 0 )
      {
      useThreshold = true;
      useSkip = false;
      }
    else if( skipSize != -1 )
      {
      useThreshold = false;
      useSkip = true;
      }
    else
      {
      useThreshold = false;
      useSkip = false;
      }

    if( useThreshold && imageItr.Get() > threshold )
      {
      doCalculation = false;
      }

    typename ImageType::IndexType curIndex;
    std::vector<int> roiCenter;
    if( doCalculation )
      {
      curIndex = imageItr.GetIndex();
      roiCenter = std::vector<int>(dimensionT);
      for( unsigned int i = 0; i < dimensionT; ++i )
        {
        if( useSkip && (curIndex[i]-start[i]) % skipSize != 0 )
          {
          doCalculation = false;
          break;
          }
        roiCenter[i] = curIndex[i];
        }
      }

    if( doCalculation )
      {
      tube::SubImageGenerator<PixelType,dimensionT> subGenerator;
      subGenerator.SetRoiCenter(roiCenter);
      subGenerator.SetRoiSize(roiSize);
      subGenerator.SetInputVolume(curImage);
      subGenerator.SetInputMask(curPrior);
      subGenerator.Update();

      tube::JointHistogramGenerator<PixelType,dimensionT> histGenerator;
      histGenerator.SetInputVolume(subGenerator.GetOutputVolume());
      histGenerator.SetInputMask(subGenerator.GetOutputMask());
      histGenerator.SetNumberOfBins(histogramSize);
      histGenerator.SetInputMin(imageMin);
      histGenerator.SetInputMax(imageMax);
      histGenerator.SetMaskMin(maskMin);
      histGenerator.SetMaskMax(maskMax);
      histGenerator.Update();
      hist = histGenerator.GetOutputVolume();

      HistIteratorType histItr( hist, hist->GetLargestPossibleRegion() );
      HistIteratorType meanItr( meanHist,
                                meanHist->GetLargestPossibleRegion() );
      HistIteratorType stdItr( stdevHist,
                               stdevHist->GetLargestPossibleRegion() );
      histItr.GoToBegin();
      meanItr.GoToBegin();
      stdItr.GoToBegin();
      typename HistogramType::PixelType val = 0;

      if( scoringMethod == std::string("histogram") )
        {
        int count = 0;
        int zHistBins = 100;
        double zMax = 10;
        int zHist[100];
        for( int i=0; i<zHistBins; i++ )
          {
          zHist[i] = 0;
          }
        while( !histItr.IsAtEnd() && !meanItr.IsAtEnd() && !stdItr.IsAtEnd() )
          {
          typename HistogramType::PixelType t = histItr.Get();
          typename HistogramType::PixelType m = meanItr.Get();
          typename HistogramType::PixelType s = stdItr.Get();
          if( s == 0 )
            {
            s = 0.0001;
            }
          double tf = vnl_math_abs(t-m)/s;
          tf = tf / zMax * zHistBins;
          if(tf >= zHistBins)
            {
            tf = zHistBins - 1;
            }
          ++zHist[ (int)tf ];
          ++count;

          ++histItr;
          ++meanItr;
          ++stdItr;
          }

        double thresh = count*0.95;
        for( int i=zHistBins-1; i>0; i-- )
          {
          count -= zHist[i];
          if( count < thresh )
            {
            val = ((i/(double)zHistBins) + 0.5) * zMax;
            break;
            }
          }
        }
      else if(scoringMethod == std::string("max"))
        {
        typename HistogramType::PixelType maxVal = 0;
        while( !histItr.IsAtEnd() && !meanItr.IsAtEnd() && !stdItr.IsAtEnd() )
          {
          typename HistogramType::PixelType t = histItr.Get();
          typename HistogramType::PixelType m = meanItr.Get();
          typename HistogramType::PixelType s = stdItr.Get();
          if( s == 0 )
            {
            s = 0.0001;
            }
          val = vnl_math_abs(t-m)/s;
          if( maxVal < val )
            {
            maxVal = val;
            }
          ++histItr;
          ++meanItr;
          ++stdItr;
          }
        val = maxVal;
        }
      else if( scoringMethod == std::string("mean") )
        {
        typename HistogramType::PixelType histCount = 0;
        while( !histItr.IsAtEnd() && !meanItr.IsAtEnd() && !stdItr.IsAtEnd() )
          {
          typename HistogramType::PixelType t = histItr.Get();
          typename HistogramType::PixelType m = meanItr.Get();
          typename HistogramType::PixelType s = stdItr.Get();
          if( s == 0 )
            {
            s = 0.0001;
            }
          val += vnl_math_abs(t-m)/s;
          ++histItr;
          ++meanItr;
          ++stdItr;
          ++histCount;
          }
        val /= histCount;
        }
      else // assume sum if nothing specified
        {
        while( !histItr.IsAtEnd() && !meanItr.IsAtEnd() && !stdItr.IsAtEnd() )
          {
          typename HistogramType::PixelType t = histItr.Get();
          typename HistogramType::PixelType m = meanItr.Get();
          typename HistogramType::PixelType s = stdItr.Get();
          if( s == 0 )
            {
            s = 0.0001;
            }
          val += vnl_math_abs(t-m)/s;
          ++histItr;
          ++meanItr;
          ++stdItr;
          }
        }

      outImage->SetPixel(curIndex,val);
      progress += proportion/samples;
      progressReporter.Report( progress );
      }
    ++imageItr;
    }
  timeCollector.Stop("Calculate Z Scores");

  // Prepare to write the output image of scores to disk
  timeCollector.Start("Save data");
  typename WriterType::Pointer writer = WriterType::New();
  writer->SetFileName( outputVolume.c_str() );
  writer->SetInput( outImage );

  // Write the output image to disk with exception handling
  try
    {
    writer->Update();
    }
  catch( itk::ExceptionObject & err )
    {
    std::cerr << "Exception caught: " << err << std::endl;
    return EXIT_FAILURE;
    }
  timeCollector.Stop("Save data");
  progress = 1.0;
  progressReporter.Report( progress );

  // Report the time each process step took
  timeCollector.Report();

  // Return with a good value
  return EXIT_SUCCESS;
}

// Main
int main( int argc, char **argv )
{
  PARSE_ARGS;

  // You may need to update this line if, in the project's .xml CLI file,
  //   you change the variable name for the inputVolume.
  return tube::ParseArgsAndCallDoIt( inputVolume, argc, argv );
}