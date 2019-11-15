#ifndef __XML_CONFIG_DEFINE_H__
#define __XML_CONFIG_DEFINE_H__
#include <map>
#include <vector>
#include "vartype.h"
#include "xmlparser.h"

namespace XmlConfig {

	template <typename T>
	void load_vector(std::string vec_name, std::string sub_nodename, std::vector<T> &var, const Fir::XMLParser &xml, const Fir::XMLParser::Node *node) {
		if (NULL == node) return;
		const Fir::XMLParser::Node *vec_node = xml.child(node, "vector");
		while (vec_node) {
			if (xml.node_attribute(vec_node, "var") == vec_name) {
				var.resize(xml.child_count(vec_node, sub_nodename.c_str()));
				const Fir::XMLParser::Node *sub_node = xml.child(vec_node, sub_nodename.c_str());
				size_t i = 0;
				while (sub_node && i < var.size()) {
					var[i].load(xml, sub_node);
					++i;
					sub_node = xml.next(sub_node, sub_nodename.c_str());
				}
				break;
			}
			vec_node = xml.next(vec_node, "vector");
		}
	}

	static void load_vartype_vector(std::string vec_name, std::vector<Fir::VarType> &var, const Fir::XMLParser &xml, const Fir::XMLParser::Node *node) {
		if (NULL == node) return;
		const Fir::XMLParser::Node *vec_node = xml.child(node, "vector");
		while (vec_node) {
			if (xml.node_attribute(vec_node, "var") == vec_name) {
				const Fir::XMLParser::Node *sub_node = xml.child(vec_node, NULL);
				while (sub_node) { 
					var.push_back(xml.node_value(sub_node));
					sub_node = xml.next(sub_node, NULL);
				}
				break;			}
			vec_node = xml.next(vec_node, "vector");
		}
	}

	struct example_t {
		public:
			struct structItem_t {
				public:
					struct item_t {
						public:
							void load(const Fir::XMLParser &xml, const Fir::XMLParser::Node *node);
							const Fir::VarType &itemid()const { return _itemid; }
							const Fir::VarType &itemvar1()const { return _itemvar1; }
							const Fir::VarType &itemvar2()const { return _itemvar2; }

						private:
							Fir::VarType _itemid;
							Fir::VarType _itemvar1;
							Fir::VarType _itemvar2;
					};

				public:
					void load(const Fir::XMLParser &xml, const Fir::XMLParser::Node *node);
					const std::map< Fir::VarType, item_t > &exampleMap()const { return _exampleMap; }
					const Fir::VarType &item1()const { return _item1; }
					const Fir::VarType &item2()const { return _item2; }

				private:
					std::map< Fir::VarType, item_t > _exampleMap;
					Fir::VarType _item1;
					Fir::VarType _item2;
			};

			struct structName_t {
				public:
					struct example_t {
						public:
							struct mapitem_t {
								public:
									void load(const Fir::XMLParser &xml, const Fir::XMLParser::Node *node);
									const Fir::VarType &id()const { return _id; }
									const Fir::VarType &va()const { return _va; }
									const Fir::VarType &vb()const { return _vb; }
									const Fir::VarType &vc()const { return _vc; }

								private:
									Fir::VarType _id;
									Fir::VarType _va;
									Fir::VarType _vb;
									Fir::VarType _vc;
							};

						public:
							void load(const Fir::XMLParser &xml, const Fir::XMLParser::Node *node);
							const std::map< Fir::VarType, mapitem_t > &exMap()const { return _exMap; }
							const Fir::VarType &exam1()const { return _exam1; }
							const Fir::VarType &exam2()const { return _exam2; }
							const Fir::VarType &exam3()const { return _exam3; }

						private:
							std::map< Fir::VarType, mapitem_t > _exMap;
							Fir::VarType _exam1;
							Fir::VarType _exam2;
							Fir::VarType _exam3;
					};

					struct item_t {
						public:
							void load(const Fir::XMLParser &xml, const Fir::XMLParser::Node *node);
							const Fir::VarType &itemid()const { return _itemid; }
							const Fir::VarType &itemvar1()const { return _itemvar1; }
							const Fir::VarType &itemvar2()const { return _itemvar2; }

						private:
							Fir::VarType _itemid;
							Fir::VarType _itemvar1;
							Fir::VarType _itemvar2;
					};

					struct structIt_t {
						public:
							void load(const Fir::XMLParser &xml, const Fir::XMLParser::Node *node);
							const Fir::VarType &it1()const { return _it1; }
							const Fir::VarType &it2()const { return _it2; }
							const Fir::VarType &it3()const { return _it3; }

						private:
							Fir::VarType _it1;
							Fir::VarType _it2;
							Fir::VarType _it3;
					};

				public:
					void load(const Fir::XMLParser &xml, const Fir::XMLParser::Node *node);
					const std::map< Fir::VarType, item_t > &exampleMap()const { return _exampleMap; }
					const std::vector< example_t > &exampleVector()const { return _exampleVector; }
					const std::vector< example_t > &firstVector()const { return _firstVector; }
					const structIt_t &structIt()const { return _structIt; }
					const Fir::VarType &var1()const { return _var1; }
					const Fir::VarType &var2()const { return _var2; }

				private:
					std::map< Fir::VarType, item_t > _exampleMap;
					std::vector< example_t > _exampleVector;
					std::vector< example_t > _firstVector;
					structIt_t _structIt;
					Fir::VarType _var1;
					Fir::VarType _var2;
			};

		public:
			void load(const Fir::XMLParser &xml, const Fir::XMLParser::Node *node);
			const structItem_t &structItem()const { return _structItem; }
			const structName_t &structName()const { return _structName; }
			const Fir::VarType &version1()const { return _version1; }
			const Fir::VarType &version2()const { return _version2; }

		private:
			structItem_t _structItem;
			structName_t _structName;
			Fir::VarType _version1;
			Fir::VarType _version2;
	};

}

#endif

