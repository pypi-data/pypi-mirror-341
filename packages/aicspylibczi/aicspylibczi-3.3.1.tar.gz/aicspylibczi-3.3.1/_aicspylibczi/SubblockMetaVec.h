//
// Created by Jamie Sherman on 2019-11-13.
//

#ifndef _PYLIBCZI_SUBBLOCKMETAVEC_H
#define _PYLIBCZI_SUBBLOCKMETAVEC_H

#include <regex>
#include <vector>

#include "Image.h"
#include "SubblockSortable.h"
#include "inc_libCZI.h"

namespace pylibczi {

class SubblockString : public SubblockSortable
{
  std::string m_string;

public:
  SubblockString(const libCZI::CDimCoordinate* plane_, int index_m_, bool is_mosaic_, char* str_p_, size_t str_size_)
    : SubblockSortable(plane_, index_m_, is_mosaic_)
    , m_string(str_p_, str_size_)
  {
    // clear string from garbage symbols
    std::regex lthan("&lt;"), gthan("&gt;"), spce("\\s*\\r\\n\\s*");
    std::regex metatag("</METADATA>.*"), quote("\\\"");
    m_string = std::regex_replace(m_string, lthan, "<");
    m_string = std::regex_replace(m_string, gthan, ">");
    m_string = std::regex_replace(m_string, spce, "");
    m_string = std::regex_replace(m_string, metatag, "</METADATA>");
    m_string += "";
  }

  std::string getString() const { return m_string; }
};

class SubblockMetaVec : public std::vector<SubblockString>
{
  bool m_isMosaic = false;

public:
  SubblockMetaVec()
    : std::vector<SubblockString>()
  {}

  void setMosaic(bool mosaic_) { m_isMosaic = mosaic_; }

  void sort()
  {
    std::sort(begin(), end(), [](SubblockString& a_, SubblockString& b_) -> bool { return a_ < b_; });
  }

  std::vector<std::pair<char, size_t>> getShape()
  {
    std::vector<std::map<char, size_t>> validIndexes;
    for (const auto& image : *this) {
      validIndexes.push_back(image.getValidIndexes(m_isMosaic)); // only add M if it's a mosaic file
    }

    // TODO This code assumes the data is a matrix, meaning for example scene's have the same number of Z-slices
    // TODO is there another way to do this that could cope with variable data sizes within the matrix?
    std::vector<std::pair<char, size_t>> charSizes;
    std::map<char, std::set<size_t>> charSetSize;
    std::map<char, std::set<size_t>>::iterator found;
    for (const auto& validMap : validIndexes) {
      for (auto keySet : validMap) {
        found = charSetSize.emplace(keySet.first, std::set<size_t>()).first;
        found->second.insert(keySet.second);
      }
    }
    for (auto keySet : charSetSize) {
      charSizes.emplace_back(keySet.first, keySet.second.size());
    }
    // sort them into descending DimensionIndex Order
    std::sort(charSizes.begin(), charSizes.end(), [&](std::pair<char, size_t> a_, std::pair<char, size_t> b_) {
      return libCZI::Utils::CharToDimension(a_.first) > libCZI::Utils::CharToDimension(b_.first);
    });
    return charSizes;
  }
};
}

#endif //_PYLIBCZI_SUBBLOCKMETAVEC_H
