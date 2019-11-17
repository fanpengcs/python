#include "xmlconfig_define.h"

namespace XmlConfig {

	void example_t::structItem_t::item_t::load(const Fir::XMLParser &xml, const Fir::XMLParser::Node *node) {
		if (!node)
			return;
		if (!xml.has_attribute(node, "itemid")) {
			const Fir::XMLParser::Node *sub = xml.child(node, "itemid");
			if (sub)
				_itemid = xml.node_value(sub);
		}
		else {
			_itemid = xml.node_attribute(node, "itemid");
		}
		if (!xml.has_attribute(node, "itemvar1")) {
			const Fir::XMLParser::Node *sub = xml.child(node, "itemvar1");
			if (sub)
				_itemvar1 = xml.node_value(sub);
		}
		else {
			_itemvar1 = xml.node_attribute(node, "itemvar1");
		}
		if (!xml.has_attribute(node, "itemvar2")) {
			const Fir::XMLParser::Node *sub = xml.child(node, "itemvar2");
			if (sub)
				_itemvar2 = xml.node_value(sub);
		}
		else {
			_itemvar2 = xml.node_attribute(node, "itemvar2");
		}
	}

	void example_t::structItem_t::load(const Fir::XMLParser &xml, const Fir::XMLParser::Node *node) {
		if (!node)
			return;
		const Fir::XMLParser::Node *map_exampleMap_node = xml.child(node, "map");
		while (map_exampleMap_node) {
			if (xml.node_attribute(map_exampleMap_node, "var") == "exampleMap") {
				Fir::VarType keyname = xml.node_attribute(map_exampleMap_node, "key");
				const Fir::XMLParser::Node *sub_node = xml.child(map_exampleMap_node, "item");
				while (sub_node) {
					_exampleMap[xml.node_attribute(sub_node, keyname)].load(xml, sub_node);
					sub_node = xml.next(sub_node, "item");
				}
				break;
			}
			map_exampleMap_node = xml.next(map_exampleMap_node, "map");
		}
		if (!xml.has_attribute(node, "item1")) {
			const Fir::XMLParser::Node *sub = xml.child(node, "item1");
			if (sub)
				_item1 = xml.node_value(sub);
		}
		else {
			_item1 = xml.node_attribute(node, "item1");
		}
		if (!xml.has_attribute(node, "item2")) {
			const Fir::XMLParser::Node *sub = xml.child(node, "item2");
			if (sub)
				_item2 = xml.node_value(sub);
		}
		else {
			_item2 = xml.node_attribute(node, "item2");
		}
	}

	void example_t::structName_t::example_t::mapitem_t::load(const Fir::XMLParser &xml, const Fir::XMLParser::Node *node) {
		if (!node)
			return;
		if (!xml.has_attribute(node, "id")) {
			const Fir::XMLParser::Node *sub = xml.child(node, "id");
			if (sub)
				_id = xml.node_value(sub);
		}
		else {
			_id = xml.node_attribute(node, "id");
		}
		if (!xml.has_attribute(node, "va")) {
			const Fir::XMLParser::Node *sub = xml.child(node, "va");
			if (sub)
				_va = xml.node_value(sub);
		}
		else {
			_va = xml.node_attribute(node, "va");
		}
		if (!xml.has_attribute(node, "vb")) {
			const Fir::XMLParser::Node *sub = xml.child(node, "vb");
			if (sub)
				_vb = xml.node_value(sub);
		}
		else {
			_vb = xml.node_attribute(node, "vb");
		}
		if (!xml.has_attribute(node, "vc")) {
			const Fir::XMLParser::Node *sub = xml.child(node, "vc");
			if (sub)
				_vc = xml.node_value(sub);
		}
		else {
			_vc = xml.node_attribute(node, "vc");
		}
	}

	void example_t::structName_t::example_t::load(const Fir::XMLParser &xml, const Fir::XMLParser::Node *node) {
		if (!node)
			return;
		const Fir::XMLParser::Node *map_exMap_node = xml.child(node, "map");
		while (map_exMap_node) {
			if (xml.node_attribute(map_exMap_node, "var") == "exMap") {
				Fir::VarType keyname = xml.node_attribute(map_exMap_node, "key");
				const Fir::XMLParser::Node *sub_node = xml.child(map_exMap_node, "mapitem");
				while (sub_node) {
					_exMap[xml.node_attribute(sub_node, keyname)].load(xml, sub_node);
					sub_node = xml.next(sub_node, "mapitem");
				}
				break;
			}
			map_exMap_node = xml.next(map_exMap_node, "map");
		}
		if (!xml.has_attribute(node, "exam1")) {
			const Fir::XMLParser::Node *sub = xml.child(node, "exam1");
			if (sub)
				_exam1 = xml.node_value(sub);
		}
		else {
			_exam1 = xml.node_attribute(node, "exam1");
		}
		if (!xml.has_attribute(node, "exam2")) {
			const Fir::XMLParser::Node *sub = xml.child(node, "exam2");
			if (sub)
				_exam2 = xml.node_value(sub);
		}
		else {
			_exam2 = xml.node_attribute(node, "exam2");
		}
		if (!xml.has_attribute(node, "exam3")) {
			const Fir::XMLParser::Node *sub = xml.child(node, "exam3");
			if (sub)
				_exam3 = xml.node_value(sub);
		}
		else {
			_exam3 = xml.node_attribute(node, "exam3");
		}
	}

	void example_t::structName_t::item_t::load(const Fir::XMLParser &xml, const Fir::XMLParser::Node *node) {
		if (!node)
			return;
		if (!xml.has_attribute(node, "itemid")) {
			const Fir::XMLParser::Node *sub = xml.child(node, "itemid");
			if (sub)
				_itemid = xml.node_value(sub);
		}
		else {
			_itemid = xml.node_attribute(node, "itemid");
		}
		if (!xml.has_attribute(node, "itemvar1")) {
			const Fir::XMLParser::Node *sub = xml.child(node, "itemvar1");
			if (sub)
				_itemvar1 = xml.node_value(sub);
		}
		else {
			_itemvar1 = xml.node_attribute(node, "itemvar1");
		}
		if (!xml.has_attribute(node, "itemvar2")) {
			const Fir::XMLParser::Node *sub = xml.child(node, "itemvar2");
			if (sub)
				_itemvar2 = xml.node_value(sub);
		}
		else {
			_itemvar2 = xml.node_attribute(node, "itemvar2");
		}
	}

	void example_t::structName_t::structIt_t::load(const Fir::XMLParser &xml, const Fir::XMLParser::Node *node) {
		if (!node)
			return;
		if (!xml.has_attribute(node, "it1")) {
			const Fir::XMLParser::Node *sub = xml.child(node, "it1");
			if (sub)
				_it1 = xml.node_value(sub);
		}
		else {
			_it1 = xml.node_attribute(node, "it1");
		}
		if (!xml.has_attribute(node, "it2")) {
			const Fir::XMLParser::Node *sub = xml.child(node, "it2");
			if (sub)
				_it2 = xml.node_value(sub);
		}
		else {
			_it2 = xml.node_attribute(node, "it2");
		}
		if (!xml.has_attribute(node, "it3")) {
			const Fir::XMLParser::Node *sub = xml.child(node, "it3");
			if (sub)
				_it3 = xml.node_value(sub);
		}
		else {
			_it3 = xml.node_attribute(node, "it3");
		}
	}

	void example_t::structName_t::load(const Fir::XMLParser &xml, const Fir::XMLParser::Node *node) {
		if (!node)
			return;
		const Fir::XMLParser::Node *map_exampleMap_node = xml.child(node, "map");
		while (map_exampleMap_node) {
			if (xml.node_attribute(map_exampleMap_node, "var") == "exampleMap") {
				Fir::VarType keyname = xml.node_attribute(map_exampleMap_node, "key");
				const Fir::XMLParser::Node *sub_node = xml.child(map_exampleMap_node, "item");
				while (sub_node) {
					_exampleMap[xml.node_attribute(sub_node, keyname)].load(xml, sub_node);
					sub_node = xml.next(sub_node, "item");
				}
				break;
			}
			map_exampleMap_node = xml.next(map_exampleMap_node, "map");
		}
		load_vector< example_t >("exampleVector", "example", _exampleVector, xml, node);
		load_vector< example_t >("firstVector", "example", _firstVector, xml, node);
		const Fir::XMLParser::Node *structIt_node = xml.child(node, "structIt");
		while (structIt_node) {
			_structIt.load(xml, structIt_node);
			structIt_node = xml.next(structIt_node, "structIt");
		}
		if (!xml.has_attribute(node, "var1")) {
			const Fir::XMLParser::Node *sub = xml.child(node, "var1");
			if (sub)
				_var1 = xml.node_value(sub);
		}
		else {
			_var1 = xml.node_attribute(node, "var1");
		}
		if (!xml.has_attribute(node, "var2")) {
			const Fir::XMLParser::Node *sub = xml.child(node, "var2");
			if (sub)
				_var2 = xml.node_value(sub);
		}
		else {
			_var2 = xml.node_attribute(node, "var2");
		}
	}

	void example_t::load(const Fir::XMLParser &xml, const Fir::XMLParser::Node *node) {
		if (!node)
			return;
		const Fir::XMLParser::Node *structItem_node = xml.child(node, "structItem");
		while (structItem_node) {
			_structItem.load(xml, structItem_node);
			structItem_node = xml.next(structItem_node, "structItem");
		}
		const Fir::XMLParser::Node *structName_node = xml.child(node, "structName");
		while (structName_node) {
			_structName.load(xml, structName_node);
			structName_node = xml.next(structName_node, "structName");
		}
		if (!xml.has_attribute(node, "version1")) {
			const Fir::XMLParser::Node *sub = xml.child(node, "version1");
			if (sub)
				_version1 = xml.node_value(sub);
		}
		else {
			_version1 = xml.node_attribute(node, "version1");
		}
		if (!xml.has_attribute(node, "version2")) {
			const Fir::XMLParser::Node *sub = xml.child(node, "version2");
			if (sub)
				_version2 = xml.node_value(sub);
		}
		else {
			_version2 = xml.node_attribute(node, "version2");
		}
	}

}

