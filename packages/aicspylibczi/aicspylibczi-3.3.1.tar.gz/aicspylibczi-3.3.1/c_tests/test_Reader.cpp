#include <algorithm>
#include <chrono>
#include <memory>
#include <sstream>

#include "catch.hpp"

#include "../_aicspylibczi/Reader.h"
#include "../_aicspylibczi/SubblockSortable.h"
#include "../_aicspylibczi/pb_helpers.h"

#include "libCZI/StreamImpl.h"

#define CORES_FOR_THREADS 1 // for local testing increase this but for GH Actions it must be 1

void
printDims(const std::string& msg, const pylibczi::Reader::DimsShape& dimsVec)
{
  std::cout << msg << std::endl;
  using DI = pylibczi::DimIndex;
  for (const auto& x : dimsVec) {
    for (const auto& y : x) {
      char yChar;
      switch (y.first) {
        case DI::X:
          yChar = 'X';
          break;
        case DI::Y:
          yChar = 'Y';
          break;
        case DI::Z:
          yChar = 'Z';
          break;
        case DI::M:
          yChar = 'M';
          break;
        case DI::C:
          yChar = 'C';
          break;
        case DI::T:
          yChar = 'T';
          break;
        case DI::V:
          yChar = 'V';
          break;
        case DI::B:
          yChar = 'B';
          break;
        case DI::S:
          yChar = 'S';
          break;
        default:
          yChar = 'N';
          break;
      }
      std::cout << yChar << "\t [ " << y.second.first << ", " << y.second.second << " ]" << std::endl;
    }
  }
}

class CziCreator
{
  std::unique_ptr<pylibczi::Reader> m_czi;

public:
  CziCreator()
    : m_czi(new pylibczi::Reader(L"resources/s_1_t_1_c_1_z_1.czi"))
  {
  }
  pylibczi::Reader* get() { return m_czi.get(); }
};

class CziCreator2
{
  std::unique_ptr<pylibczi::Reader> m_czi;

public:
  CziCreator2()
    : m_czi(new pylibczi::Reader(L"resources/s_3_t_1_c_3_z_5.czi"))
  {
  }
  pylibczi::Reader* get() { return m_czi.get(); }
};

class CziCreatorOrder
{
  std::unique_ptr<pylibczi::Reader> m_czi;

public:
  CziCreatorOrder()
    : m_czi(new pylibczi::Reader(L"resources/CD_s_1_t_3_c_2_z_5.czi"))
  {
  }
  pylibczi::Reader* get() { return m_czi.get(); }
};

class CziCreatorIStream
{
  std::unique_ptr<pylibczi::Reader> m_czi;

public:
  CziCreatorIStream()
    : m_czi()
  {
    auto fp = std::shared_ptr<libCZI::IInputOutputStream>(
      libCZI::CreateInputOutputStreamForFile(L"resources/s_1_t_1_c_1_z_1.czi"));
    m_czi = std::make_unique<pylibczi::Reader>(fp);
  }
  pylibczi::Reader* get() { return m_czi.get(); }
};

#ifdef LOCAL_TEST

class CziCreatorBig
{
  std::unique_ptr<pylibczi::Reader> m_czi;

public:
  CziCreatorBig()
    : m_czi(new pylibczi::Reader(L"/Users/jamies/Data/20190425_S08_001-04-Scene-4-P3-B03.czi"))
  {
  }
  pylibczi::Reader* get() { return m_czi.get(); }
};

class CziCreatorBigM
{
  std::unique_ptr<pylibczi::Reader> m_czi;

public:
  CziCreatorBigM()
    : m_czi(new pylibczi::Reader(L"/Users/jamies/Data/20190614_C01_001.czi"))
  {
  }
  pylibczi::Reader* get() { return m_czi.get(); }
};
#endif

class CziCreator4
{
  std::unique_ptr<pylibczi::Reader> m_czi;

public:
  CziCreator4()
    : m_czi(new pylibczi::Reader(L"resources/s_1_t_10_c_3_z_1.czi"))
  {
  }
  pylibczi::Reader* get() { return m_czi.get(); }
};

class CziCreator5
{
  std::unique_ptr<pylibczi::Reader> m_czi;

public:
  CziCreator5()
    : m_czi(new pylibczi::Reader(L"resources/Multiscene_CZI_3Scenes.czi"))
  {
  }
  pylibczi::Reader* get() { return m_czi.get(); }
};

class CziCreatorTiles
{
  std::unique_ptr<pylibczi::Reader> m_czi;

public:
  CziCreatorTiles()
    : m_czi(new pylibczi::Reader(L"resources/tiles.czi"))
  {
  }
  pylibczi::Reader* get() { return m_czi.get(); }
};

class CziCreatorTilesTZ
{
  std::unique_ptr<pylibczi::Reader> m_czi;

public:
  CziCreatorTilesTZ()
    : m_czi(new pylibczi::Reader(L"resources/tiles_time_z.czi"))
  {
  }
  pylibczi::Reader* get() { return m_czi.get(); }
};

class CziCreatorTilesZ
{
  std::unique_ptr<pylibczi::Reader> m_czi;

public:
  CziCreatorTilesZ()
    : m_czi(new pylibczi::Reader(L"resources/tiles_z.czi"))
  {
  }
  pylibczi::Reader* get() { return m_czi.get(); }
};

TEST_CASE_METHOD(CziCreatorIStream, "test_reader_constructor", "[Reader]")
{
  REQUIRE_NOTHROW(get());
}

TEST_CASE("open_two_czis", "[Reader_Dup]")
{
  REQUIRE_NOTHROW(pylibczi::Reader(L"resources/s_1_t_1_c_1_z_1.czi"));
  REQUIRE_NOTHROW(pylibczi::Reader(L"resources/s_1_t_1_c_1_z_1.czi"));
}

TEST_CASE_METHOD(CziCreator, "test_reader_dims_1", "[Reader_Dims]")
{
  using DI = pylibczi::DimIndex;
  pylibczi::Reader::DimsShape ans{
    { { DI::X, { 0, 475 } }, { DI::Y, { 0, 325 } }, { DI::C, { 0, 1 } }, { DI::B, { 0, 1 } } },
  };
  auto czi = get();
  auto dimsVec = czi->readDimsRange();
  REQUIRE(czi->shapeIsConsistent());
  REQUIRE(dimsVec.size() == 1);
  REQUIRE(dimsVec == ans);
}

TEST_CASE_METHOD(CziCreator, "test_reader_dims_2", "[Reader_Dims_String]")
{
  auto czi = get();
  auto dims = czi->dimsString();
  REQUIRE(dims == std::string("BCYX")); // B=0, C=0 for this file
}

TEST_CASE_METHOD(CziCreator2, "test_reader_dims_3", "[Reader_Dims_Size]")
{
  auto czi = get();
  std::string dstr = czi->dimsString();
  auto dims = czi->dimSizes();
  std::vector<int> shape = { 1, 3, 3, 5, 325, 475 };
  REQUIRE(czi->shapeIsConsistent());
  REQUIRE(dstr == "BSCZYX");
  REQUIRE(dims == shape);
}

TEST_CASE_METHOD(CziCreator, "test_is_mosaic", "[Reader_Is_Mosaic]")
{
  auto czi = get();
  REQUIRE(!czi->isMosaic());
}

TEST_CASE_METHOD(CziCreator, "test_meta_reader", "[Reader_read_meta]")
{
  auto czi = get();
  std::string xml = czi->readMeta();
  std::string ans("<?xml version=\"1.0\"?>\n"
                  "<ImageDocument>\n"
                  " <Metadata>\n"
                  "  <Experiment Version=\"1.1\">\n"
                  "   "
                  "<RunMode>OptimizeBeforePerformEnabled,"
                  "ValidateAndAdaptBeforePerformEnabled</RunMode>");
  REQUIRE(std::strncmp(ans.c_str(), xml.c_str(), ans.size()) == 0);
}

TEST_CASE_METHOD(CziCreator, "test_read_selected", "[Reader_read_selected]")
{
  auto czi = get();
  auto cDims = libCZI::CDimCoordinate{ { libCZI::DimensionIndex::B, 0 }, { libCZI::DimensionIndex::C, 0 } };
  auto imCont = czi->readSelected(cDims, -1, CORES_FOR_THREADS);
  auto imvec = imCont.first->images();
  REQUIRE(imvec.size() == 1);
  auto shape = imvec.front()->shape();
  REQUIRE(shape[0] == 325); // height
  REQUIRE(shape[1] == 475); // width
}

TEST_CASE_METHOD(CziCreator2, "test_read_selected2", "[Reader_read_selected]")
{
  auto czi = get();
  auto cDims = libCZI::CDimCoordinate{ { libCZI::DimensionIndex::B, 0 }, { libCZI::DimensionIndex::C, 0 } };
  auto imCont = czi->readSelected(cDims, -1, CORES_FOR_THREADS);
  auto imvec = imCont.first->images();
  REQUIRE(imvec.size() == 15);
  auto shape = imvec.front()->shape();
  REQUIRE(shape[0] == 325); // height
  REQUIRE(shape[1] == 475); // width
}

TEST_CASE_METHOD(CziCreatorIStream, "test_read_selected3", "[Reader_read_selected]")
{
  auto czi = get();
  auto cDims = libCZI::CDimCoordinate{ { libCZI::DimensionIndex::C, 0 } };
  auto imCont = czi->readSelected(cDims, -1, CORES_FOR_THREADS);
  auto imvec = imCont.first->images();
  REQUIRE(imvec.size() == 1);
  auto shape = imvec.front()->shape();
  REQUIRE(shape[0] == 325); // height
  REQUIRE(shape[1] == 475); // width
}

TEST_CASE_METHOD(CziCreatorIStream, "test_read_selected4", "[Reader_read_selected]")
{
  auto czi = get();
  auto cDims = libCZI::CDimCoordinate();
  auto imCont = czi->readSelected(cDims, -1, CORES_FOR_THREADS);
  auto imvec = imCont.first->images();
  REQUIRE(imvec.size() == 1);
  auto shape = imvec.front()->shape();
  REQUIRE(shape[0] == 325); // height
  REQUIRE(shape[1] == 475); // width
}

TEST_CASE_METHOD(CziCreator2, "test_bad_scene", "[Reader_read_bad_scene]")
{
  auto czi = get();
  auto cDims = libCZI::CDimCoordinate{ { libCZI::DimensionIndex::B, 0 },
                                       { libCZI::DimensionIndex::C, 0 },
                                       { libCZI::DimensionIndex::S, 4 } };
  REQUIRE_THROWS_AS(czi->readSelected(cDims, -1, CORES_FOR_THREADS), pylibczi::CDimCoordinatesOverspecifiedException);
}

TEST_CASE_METHOD(CziCreator2, "test_read_subblock_meta", "[Reader_read_subblock_meta]")
{
  auto czi = get();
  auto cDims = libCZI::CDimCoordinate{ { libCZI::DimensionIndex::B, 0 }, { libCZI::DimensionIndex::C, 0 } };
  auto metavec = czi->readSubblockMeta(cDims);
  REQUIRE(metavec.size() == 15);
  auto test = pb_helpers::packStringArray(metavec);
  int x = 10;
}

class CziMCreator
{
  std::unique_ptr<pylibczi::Reader> m_czi;

public:
  CziMCreator()
    : m_czi(new pylibczi::Reader(L"resources/mosaic_test.czi"))
  {
  }
  pylibczi::Reader* get() { return m_czi.get(); }
};

TEST_CASE_METHOD(CziMCreator, "test_mosaic_is_mosaic", "[Reader_mosaic_is_mosaic]")
{
  auto czi = get();
  REQUIRE(czi->isMosaic());
}

TEST_CASE_METHOD(CziMCreator, "test_mosaic_dims", "[Reader_mosaic_dims]")
{
  auto czi = get();
  REQUIRE(czi->dimsString() == std::string("STCZMYX"));
}

TEST_CASE_METHOD(CziMCreator, "test_mosaic_dimsSize", "[Reader_mosaic_dimsSize]")
{
  auto czi = get();
  std::vector<int> ans{ 1, 1, 1, 1, 2, 624, 924 };
  REQUIRE(czi->dimSizes() == ans);
}

TEST_CASE_METHOD(CziMCreator, "test_mosaic_readdims", "[Reader_mosaic_readdims]")
{
  auto czi = get();
  using DI = pylibczi::DimIndex;
  pylibczi::Reader::DimsShape ans{ { { DI::S, { 0, 1 } },
                                     { DI::T, { 0, 1 } },
                                     { DI::C, { 0, 1 } },
                                     { DI::Z, { 0, 1 } },
                                     { DI::M, { 0, 2 } },
                                     { DI::Y, { 0, 624 } },
                                     { DI::X, { 0, 924 } } } };
  auto val = czi->readDimsRange();
  REQUIRE(val == ans);
}

TEST_CASE_METHOD(CziMCreator, "test_mosaic_readSelected", "[Reader_mosaic_readSelected]")
{
  auto czi = get();
  REQUIRE(czi->dimsString() == std::string("STCZMYX"));
  auto sze = czi->dimSizes();
  std::vector<int> szeAns{ 1, 1, 1, 1, 2, 624, 924 };
  REQUIRE(sze == szeAns);
  libCZI::CDimCoordinate c_dims;
  auto imCont = czi->readSelected(c_dims, -1, CORES_FOR_THREADS);
  auto imvec = imCont.first->images();
  REQUIRE(imvec.size() == 2);
}

TEST_CASE_METHOD(CziMCreator, "test_mosaic_read", "[Reader_mosaic_read]")
{
  auto czi = get();
  auto c_dims = libCZI::CDimCoordinate{ { libCZI::DimensionIndex::C, 0 } };
  auto imCont = czi->readMosaic(c_dims);
  auto imvec = imCont->images();
  REQUIRE(imvec.size() == 1);
}

TEST_CASE_METHOD(CziMCreator, "test_mosaic_readScaled", "[Reader_mosaic_readScaled]")
{
  auto czi = get();
  auto c_dims = libCZI::CDimCoordinate{ { libCZI::DimensionIndex::C, 0 } };
  auto imCont = czi->readMosaic(c_dims, 0.1f);
  auto imvec = imCont->images();
  REQUIRE(imvec.size() == 1);
}

TEST_CASE_METHOD(CziMCreator, "test_mosaic_shape", "[Reader_mosaic_shape]")
{
  auto czi = get();
  auto bbox = czi->mosaicBoundingBox();
  REQUIRE(bbox.w == 1756);
  REQUIRE(bbox.h == 624);
}

TEST_CASE_METHOD(CziMCreator, "test_mosaic_throw", "[Reader_mosaic_throw]")
{
  auto czi = get();
  libCZI::CDimCoordinate c_dims;
  REQUIRE_THROWS_AS(czi->readMosaic(c_dims), pylibczi::CDimCoordinatesUnderspecifiedException);
}

class CziBgrCreator
{
  std::unique_ptr<pylibczi::Reader> m_czi;
  std::vector<int> m_firstPlaneFirstTen = { 7, 6, 5, 6, 6, 7, 7, 7, 7, 7 };
  std::vector<int> m_secondPlaneFirstTen = { 14, 8, 5, 4, 4, 5, 5, 5, 5, 5 };
  // y=0, x=0:10
public:
  CziBgrCreator()
    : m_czi(new pylibczi::Reader(L"resources/RGB-8bit.czi"))
  {
  }
  pylibczi::Reader* get() { return m_czi.get(); }
  const std::vector<int>& planeZeroFirstTen() { return m_firstPlaneFirstTen; }
  const std::vector<int>& planeOneFirstTen() { return m_secondPlaneFirstTen; }
};

TEST_CASE_METHOD(CziBgrCreator, "test_bgr_read", "[Reader_read_bgr]")
{
  auto czi = get();
  libCZI::CDimCoordinate dm;
  auto imgCont = czi->readSelected(dm, -1, CORES_FOR_THREADS);
  auto pr = imgCont.first->images();

  REQUIRE(czi->dimsString() == std::string("TYXA"));
  std::vector<int> ansSize{ 1, 624, 924, 3 };
  REQUIRE(czi->dimSizes() == ansSize);

  using DI = pylibczi::DimIndex;
  pylibczi::Reader::DimsShape ansDims{
    { { DI::T, { 0, 1 } }, { DI::Y, { 0, 624 } }, { DI::X, { 0, 924 } }, { DI::A, { 0, 3 } } }
  };
  auto dims = czi->readDimsRange();
  REQUIRE(!dims.empty());
  REQUIRE(dims == ansDims);

  REQUIRE(pr.size() == 1);
  REQUIRE(pr.front()->shape() == std::vector<size_t>{ 624, 924, 3 });
  REQUIRE(pr.front()->pixelType() == libCZI::PixelType::Gray8);
}

TEST_CASE_METHOD(CziBgrCreator, "test_bgr_flatten", "[Reader_read_flatten_bgr]")
{
  auto czi = get();

  auto dims = czi->readDimsRange();

  libCZI::CDimCoordinate dm;
  auto imgCont = czi->readSelected(dm, -1, CORES_FOR_THREADS);
  auto pr = imgCont.first->images();
  auto shape = imgCont.second;
  REQUIRE(pr.size() == 1);

  std::vector<std::pair<char, size_t>> dimsTwo = pr.getShape();
  std::vector<std::pair<char, size_t>> dimsTwoAns = { { 'T', 1 }, { 'Y', 624 }, { 'X', 924 }, { 'A', 3 } };
  REQUIRE(dimsTwo == dimsTwoAns);
  for (const auto& x : pr) {
    REQUIRE(x->shape()[0] == 624);
    REQUIRE(x->shape()[1] == 924);
    REQUIRE(x->shape()[2] == 3);
  }

  pylibczi::Reader::Shape shapeAns{ { 'T', 1 }, { 'Y', 624 }, { 'X', 924 }, { 'A', 3 } };

  REQUIRE(shape == shapeAns);
  REQUIRE(pr.front()->pixelType() == libCZI::PixelType::Gray8);

  // [7, 6, 5, 6, 6, 7, 7, 7, 7, 7]
  auto timage = pylibczi::ImageFactory::getDerived<uint8_t>(pr.front());
  uint8_t* tmp = timage->getRawPtr();
  std::vector<uint8_t> data(tmp, tmp + 40);
  auto planeZero = planeZeroFirstTen();
  auto planeOne = planeOneFirstTen();
  // check data values
  for (size_t i = 0; i < 10; i++) {
    REQUIRE(data[3 * i] == planeZero[i]);
    REQUIRE(data[3 * i + 1] == planeOne[i]);
  }
}

TEST_CASE_METHOD(CziMCreator, "test_reader_mosaic_subblockinforect", "[Reader_Mosaic_SubblockInfo_Rect]")
{
  auto czi = get();

  std::vector<libCZI::IntRect> answers{ { 0, 0, 924, 624 }, { 832, 0, 924, 624 } };

  libCZI::CDimCoordinate dm;
  for (int m_index = 0; m_index < 2; m_index++) {
    auto rect = czi->mosaicTileBoundingBox(dm, m_index);
    auto answer = answers[m_index];
    REQUIRE(rect.second.x == answer.x);
    REQUIRE(rect.second.y == answer.y);
    REQUIRE(rect.second.w == answer.w);
    REQUIRE(rect.second.h == answer.h);
  }
  int invalid_m = 2;
  REQUIRE_THROWS_AS(czi->mosaicTileBoundingBox(dm, invalid_m), pylibczi::CDimCoordinatesOverspecifiedException);
}

TEST_CASE_METHOD(CziCreator2, "test_reader_subblockinforect", "[Reader_Std_SubblockInfo_Rect]")
{
  auto czi = get();

  std::vector<libCZI::IntRect> answers{ { 39850, 35568, 475, 325 },
                                        { 44851, 35568, 475, 325 },
                                        { 39850, 39272, 475, 325 } };

  for (int s_index = 0; s_index < 3; s_index++) {
    libCZI::CDimCoordinate dm{ { libCZI::DimensionIndex::S, s_index } };
    auto rects = czi->tileBoundingBoxes(dm);
    auto ans = answers[s_index];
    REQUIRE(rects.begin()->second.x == ans.x);
    REQUIRE(rects.begin()->second.y == ans.y);
    REQUIRE(rects.begin()->second.w == ans.w);
    REQUIRE(rects.begin()->second.h == ans.h);
  }

  libCZI::CDimCoordinate invalid_dim{ { libCZI::DimensionIndex::S, 5 } };
  REQUIRE_THROWS_AS(czi->tileBoundingBoxes(invalid_dim), pylibczi::CDimCoordinatesOverspecifiedException);
}

// Test multichannel BGR
class CziBgrCreator2
{
  std::unique_ptr<pylibczi::Reader> m_czi;

public:
  CziBgrCreator2()
    : m_czi(new pylibczi::Reader(L"resources/RGB-multichannel.czi"))
  {
  }
  pylibczi::Reader* get() { return m_czi.get(); }
};

TEST_CASE_METHOD(CziBgrCreator2, "test_bgr2_read", "[Reader_read_bgr2]")
{
  auto czi = get();
  libCZI::CDimCoordinate dm =
    libCZI::CDimCoordinate{ { libCZI::DimensionIndex::B, 0 }, { libCZI::DimensionIndex::C, 4 } };
  auto imgCont = czi->readSelected(dm, -1, CORES_FOR_THREADS);
  auto pr = imgCont.first->images();
  auto shape = imgCont.second;

  REQUIRE(czi->dimsString() == std::string("SCYXA"));
  std::vector<int> ansSize{ 1, 7, 81, 147, 3 };
  REQUIRE(czi->dimSizes() == ansSize);

  using DI = pylibczi::DimIndex;
  pylibczi::Reader::DimsShape ansDims{
    { { DI::S, { 0, 1 } }, { DI::C, { 0, 7 } }, { DI::Y, { 0, 81 } }, { DI::X, { 0, 147 } }, { DI::A, { 0, 3 } } }
  };
  auto dims = czi->readDimsRange();
  REQUIRE(!dims.empty());
  REQUIRE(dims == ansDims);

  REQUIRE(pr.size() == 1);
  REQUIRE(pr.front()->shape() == std::vector<size_t>{ 81, 147, 3 });
  REQUIRE(pr.front()->pixelType() == libCZI::PixelType::Gray8);
  auto c_pair = std::find_if(shape.begin(), shape.end(), [](const std::pair<char, int>& a) { return a.first == 'C'; });
  // TODO: Figure out how to report channels in BGR Images.
}

TEST_CASE_METHOD(CziBgrCreator2, "test_bgr2_flatten", "[Reader_read_flatten_bgr2]")
{
  auto czi = get();

  using pDI = pylibczi::DimIndex;
  auto dims = czi->readDimsRange();
  pylibczi::Reader::DimsShape ans = {
    { { pDI::S, { 0, 1 } }, { pDI::C, { 0, 7 } }, { pDI::Y, { 0, 81 } }, { pDI::X, { 0, 147 } }, { pDI::A, { 0, 3 } } }
  };

  REQUIRE(dims == ans);
  libCZI::CDimCoordinate dm = libCZI::CDimCoordinate{ { libCZI::DimensionIndex::C, 4 } };
  auto imgCont = czi->readSelected(dm, -1, CORES_FOR_THREADS);
  auto pr = imgCont.first->images();
  auto shape = imgCont.second;

  REQUIRE(pr.size() == 1);

  for (const auto& x : pr) {
    REQUIRE(x->shape()[0] == 81);
    REQUIRE(x->shape()[1] == 147);
    REQUIRE(x->shape()[2] == 3);
  }

  pylibczi::Reader::Shape shapeAns{ { 'S', 1 }, { 'C', 1 }, { 'Y', 81 }, { 'X', 147 }, { 'A', 3 } };
  REQUIRE(shape == shapeAns);
  REQUIRE(pr.front()->pixelType() == libCZI::PixelType::Gray8);
}

TEST_CASE_METHOD(CziBgrCreator2, "test_bgr_7channel", "[Reader_bgr_7channel]")
{
  auto czi = get();
  libCZI::CDimCoordinate dm;
  auto imCont = czi->readSelected(dm, -1, CORES_FOR_THREADS);
  auto images = imCont.first->images();
  auto shape = imCont.second;
  pylibczi::Reader::Shape shapeAns{ { 'S', 1 }, { 'C', 7 }, { 'Y', 81 }, { 'X', 147 }, { 'A', 3 } };
  REQUIRE(shape == shapeAns);
}

TEST_CASE_METHOD(CziCreator5, "test_multiscene_mosaic_bboxes", "[Reader_mosaic_bboxes]")
{
  auto czi = get();
  auto dSizes = czi->dimSizes();

  libCZI::CDimCoordinate cDim = libCZI::CDimCoordinate{ { libCZI::DimensionIndex::S, 0 } };
  auto ans = czi->tileBoundingBoxes(cDim);
  REQUIRE(ans.size() == 4); // 2 channels * 44 m_index
  // 495643, 354924, 256, 256
  pylibczi::Reader::TileBBoxMap::const_iterator ansItt = ans.begin();
  ansItt++;
  ansItt++;
  REQUIRE(ansItt->second.x == 495643);
  REQUIRE(ansItt->second.y == 354924);
  REQUIRE(ansItt->second.w == 256);
  REQUIRE(ansItt->second.h == 256);
  REQUIRE(ansItt->first.mIndex() == 2);
}

TEST_CASE_METHOD(CziCreatorOrder, "test_image_overspeced", "[Reader_image_overspeced]")
{
  auto czi = get();

  libCZI::CDimCoordinate dm = { { libCZI::DimensionIndex::C, 3 } };
  REQUIRE_THROWS_AS(czi->readSelected(dm, -1, CORES_FOR_THREADS), pylibczi::CDimCoordinatesOverspecifiedException);
}

TEST_CASE_METHOD(CziCreatorOrder, "test_image_order", "[Reader_image_order]")
{
  auto czi = get();

  libCZI::CDimCoordinate dm;
  auto imCont = czi->readSelected(dm, -1, CORES_FOR_THREADS);
  pylibczi::ImagesContainerBase* icon = imCont.first.get();
  auto images = icon->images();
  std::shared_ptr<pylibczi::Image>& last_im = images[0];
  for_each(imCont.first->images().begin() + 1,
           imCont.first->images().end(),
           [&last_im](std::shared_ptr<pylibczi::Image>& img) {
             REQUIRE(0 < ((int)(img->ptr_address() - last_im->ptr_address())));
             REQUIRE(pylibczi::SubblockSortable::aLessThanB(*last_im->coordinatePtr(), *img->coordinatePtr()));
             last_im = img;
           });
}

TEST_CASE_METHOD(CziCreatorTiles, "test_tile_no_scene", "[Reader_tile_no_scene]")
{
  auto czi = get();

  REQUIRE(czi->isMosaic());

  auto dims = czi->dimsString();
  REQUIRE(dims == std::string("BVTCZMYX"));

  auto dSizes = czi->dimSizes();
  std::vector<int> dSizesAns = { 1, 1, 1, 2, 1, 4, 256, 256 };
  REQUIRE(dSizes == dSizesAns);

  using DI = pylibczi::DimIndex;
  pylibczi::Reader::DimsShape ans{
    { { DI::X, { 0, 256 } },
      { DI::Y, { 0, 256 } },
      { DI::M, { 0, 4 } },
      { DI::Z, { 0, 1 } },
      { DI::C, { 0, 2 } },
      { DI::T, { 0, 1 } },
      { DI::V, { 0, 1 } },
      { DI::B, { 0, 1 } } },
  };

  auto dimsVec = czi->readDimsRange();
  REQUIRE(czi->shapeIsConsistent());
  REQUIRE(dimsVec.size() == 1);
  REQUIRE(dimsVec == ans);

  libCZI::CDimCoordinate dm = { { libCZI::DimensionIndex::C, 0 } };
  REQUIRE_NOTHROW(czi->readMosaic(dm));

  REQUIRE_NOTHROW(czi->readSelected(dm));
}

TEST_CASE_METHOD(CziCreatorTilesTZ, "test_tile_tz_no_scene", "[Reader_tile_tz_no_scene]")
{
  auto czi = get();

  REQUIRE(czi->isMosaic());

  auto dims = czi->dimsString();
  REQUIRE(dims == std::string("BVTCZMYX"));

  auto dSizes = czi->dimSizes();
  std::vector<int> dSizesAns = { 1, 1, 2, 2, 2, 4, 256, 256 };
  REQUIRE(dSizes == dSizesAns);

  using DI = pylibczi::DimIndex;
  pylibczi::Reader::DimsShape ans{
    { { DI::X, { 0, 256 } },
      { DI::Y, { 0, 256 } },
      { DI::M, { 0, 4 } },
      { DI::Z, { 0, 2 } },
      { DI::C, { 0, 2 } },
      { DI::T, { 0, 2 } },
      { DI::V, { 0, 1 } },
      { DI::B, { 0, 1 } } },
  };

  auto dimsVec = czi->readDimsRange();
  REQUIRE(czi->shapeIsConsistent());
  REQUIRE(dimsVec.size() == 1);
  REQUIRE(dimsVec == ans);

  libCZI::CDimCoordinate dm = { { libCZI::DimensionIndex::C, 0 },
                                { libCZI::DimensionIndex::Z, 1 },
                                { libCZI::DimensionIndex::T, 0 } };
  REQUIRE_NOTHROW(czi->readMosaic(dm));
}

TEST_CASE_METHOD(CziCreatorTilesZ, "test_tile_z_no_scene", "[Reader_tile_z_no_scene]")
{
  auto czi = get();

  REQUIRE(czi->isMosaic());

  auto dims = czi->dimsString();
  REQUIRE(dims == std::string("BVTCZMYX"));

  auto dSizes = czi->dimSizes();
  std::vector<int> dSizesAns = { 1, 1, 1, 2, 2, 4, 256, 256 };
  REQUIRE(dSizes == dSizesAns);

  using DI = pylibczi::DimIndex;
  pylibczi::Reader::DimsShape ans{
    { { DI::X, { 0, 256 } },
      { DI::Y, { 0, 256 } },
      { DI::M, { 0, 4 } },
      { DI::Z, { 0, 2 } },
      { DI::C, { 0, 2 } },
      { DI::T, { 0, 1 } },
      { DI::V, { 0, 1 } },
      { DI::B, { 0, 1 } } },
  };

  auto dimsVec = czi->readDimsRange();
  REQUIRE(czi->shapeIsConsistent());
  REQUIRE(dimsVec.size() == 1);
  REQUIRE(dimsVec == ans);

  libCZI::CDimCoordinate dm = { { libCZI::DimensionIndex::C, 0 }, { libCZI::DimensionIndex::Z, 1 } };
  REQUIRE_NOTHROW(czi->readMosaic(dm));

  REQUIRE_NOTHROW(czi->readSelected(dm));
}

#ifdef LOCAL_TEST

TEST_CASE_METHOD(CziCreatorBig, "test_big_czifile", "[Reader_timed_read]")
{
  auto czi = get();
  libCZI::CDimCoordinate dm = libCZI::CDimCoordinate{ { libCZI::DimensionIndex::B, 0 },
                                                      { libCZI::DimensionIndex::S, 0 },
                                                      { libCZI::DimensionIndex::T, 1 },
                                                      { libCZI::DimensionIndex::Z, 5 } };

  std::stringstream info("Dims: ");
  info << czi->dimsString();
  INFO(info.str());
  auto dSizes = czi->dimSizes();

  std::stringstream dsizes("Shape: {");
  for_each(dSizes.begin(), dSizes.end(), [&dsizes](const int& x) { dsizes << x << ", "; });
  dsizes << "}" << std::endl;
  INFO(dsizes.str());

  auto start = std::chrono::high_resolution_clock::now();
  auto imgCont = czi->readSelected(dm, -1, CORES_FOR_THREADS);
  auto done = std::chrono::high_resolution_clock::now();

  std::cout << "Duration(milliseconds): "
            << std::chrono::duration_cast<std::chrono::milliseconds>(done - start).count();
  REQUIRE(std::chrono::duration_cast<std::chrono::milliseconds>(done - start).count() < 5050);
}

TEST_CASE_METHOD(CziCreatorBigM, "test_bigm_czifile", "[Reader_bbox]")
{
  auto czi = get();
  auto dSizes = czi->dimSizes();

  auto ans = czi->getAllSceneYXSize(0, true);
  REQUIRE(ans.size() == 88); // 2 channels * 44 m_index
  REQUIRE(ans[2].x == 23594);
  REQUIRE(ans[2].y == 19201);
  REQUIRE(ans[2].w == 950);
  REQUIRE(ans[2].h == 650);
  libCZI::CDimCoordinate cdims = { { libCZI::DimensionIndex::C, 0 } };
  // REQUIRE_NOTHROW not compatible with MSVC as is.
}

#endif
