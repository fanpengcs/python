#include "xmlconfig.h"
#include "zLogger.h"

namespace XmlConfig {

	static std::map<std::string, bool (*)(const XmlConfig::ReadXmlFunc &)> fileResetMap = std::map<std::string, bool (*) (const XmlConfig::ReadXmlFunc &)>();

	static example_t *_example = NULL;

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
		if (_example) {
		delete _example;
			_example = NULL;
		}
		_example = new example_t;
		_example->load(xml, func(xml, "example.xml"));
		zLogger::debug("[XML配置], 加载 example.xml 成功");
		fileResetMap.insert(std::make_pair("example", resetexample));
	}

	const example_t &example() {
		if (NULL == _example)
		{
			zLogger::debug("[XML配置], 加载 ExampleSecond.xml 未初始化");
			_example = new example_t();
		}
		return *_example;
	}
	bool resetexample(const XmlConfig::ReadXmlFunc &func) {
		Fir::XMLParser xml;
		if (_example) {
			delete _example;
			_example = NULL;
		}
		_example = new example_t;
		_example->load(xml, func(xml, "example.xml"));
		zLogger::debug("[XML配置] 加载 example.xml 成功");
		return true;
	}

}

