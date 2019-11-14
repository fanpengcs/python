#ifndef __XML_CONFIG_H__
#define __XML_CONFIG_H__
#include <functional>
#include "xmlconfig_define.h"

namespace XmlConfig {

	typedef std::function<const Fir::XMLParser::Node *(Fir::XMLParser &, const char *)>	ReadXmlFunc;

	bool existConfig(const std::string &fileName);

	bool loadConfig(const std::string &fileName, const XmlConfig::ReadXmlFunc &fun);

	void init(const XmlConfig::ReadXmlFunc &func);

}

#endif

