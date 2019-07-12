#include "xmlconfig.h"
#include "zLogger.h"

namespace XmlConfig {

	static std::map<std::string, bool (*)(const XmlConfig::ReadXmlFunc &)> fileResetMap = std::map<std::string, bool (*) (const XmlConfig::ReadXmlFunc &)>();


	bool existConfig(const std::string &fileName) {
		return fileResetMap.find(fileName) != fileResetMap.end();
	}

	bool loadConfig(const std::string &fileName, const XmlConfig::ReadXmlFunc &func) {
		const auto iter = fileResetMap.find(fileName);
		if (iter != fileResetMap.end())
			return iter->second(func);
		return false;
	}

	void init(const XmlConfig::ReadXmlFunc &func) {
		fileResetMap.clear();
		Fir::XMLParser xml;
	}

}

