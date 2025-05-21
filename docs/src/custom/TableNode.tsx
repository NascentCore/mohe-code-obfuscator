import { $createTableNode, SerializedTableNode, TableNode } from '@lexical/table';

export class CustomTableNode extends TableNode {
  static getType() {
    return 'customTable';
  }

  static clone(node: CustomTableNode): CustomTableNode {
    return new CustomTableNode(node.__key);
  }


  static importJSON(serializedNode: SerializedTableNode): TableNode {
    return $createTableNode().updateFromJSON(serializedNode);
  }

  createDOM(config: any): HTMLElement {
    const wrapper = document.createElement('div');
    wrapper.className = 'ExampleEditorTheme__tableScrollableWrapper';
    const tableElement = super.createDOM(config);
    wrapper.appendChild(tableElement);

    return wrapper;
  }
}
