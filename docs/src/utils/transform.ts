// lexicalJsonToHtml.ts

import { $getRoot, $insertNodes, EditorThemeClasses, SerializedEditorState } from 'lexical'
import { $generateHtmlFromNodes, $generateNodesFromDOM } from '@lexical/html'
import { TRANSFORMERS, $convertToMarkdownString } from '@lexical/markdown'
import { setupDomEnvironment } from './setupDom'
import {createHeadlessEditor} from '@lexical/headless';
import { HeadingNode } from '@lexical/rich-text';
import { ListNode, ListItemNode } from '@lexical/list';
import {
  TableCellNode,
  TableNode,
  TableRowNode,
} from '@lexical/table';
import { CustomTableNode } from '../custom/TableNode';
import { JSDOM } from 'jsdom';

const theme:EditorThemeClasses = {
  heading: {
    h1: 'glyf-editor-h1',
    h2: 'glyf-editor-h2',
    h3: 'glyf-editor-h3'
  },
  text: {
    bold: 'glyf-editor-bold',
    italic: 'glyf-editor-italic',
    underline: 'glyf-editor-underline',
    strikethrough: 'glyf-editor-strikethrough',
    underlineStrikethrough: 'glyf-editor-underlineStrikethrough'
  },
  list: {
    listitem: 'editor-listitem',
    nested: {
      listitem: 'editor-nested-listitem',
    },
    ol: 'editor-list-ol',
    ul: 'editor-list-ul',
  },
  table: 'ExampleEditorTheme__table',
  tableCell: 'ExampleEditorTheme__tableCell',
  tableCellActionButton: 'ExampleEditorTheme__tableCellActionButton',
  tableCellActionButtonContainer:
    'ExampleEditorTheme__tableCellActionButtonContainer',
  tableCellHeader: 'ExampleEditorTheme__tableCellHeader',
  tableCellResizer: 'ExampleEditorTheme__tableCellResizer',
  tableCellSelected: 'ExampleEditorTheme__tableCellSelected',
  tableScrollableWrapper: 'ExampleEditorTheme__tableScrollableWrapper',
  tableSelected: 'ExampleEditorTheme__tableSelected',
  tableSelection: 'ExampleEditorTheme__tableSelection',
};

function onError(error: Error): void {
  console.error(error);
}


const initialConfig = {
  namespace: 'MyEditor',
  theme,
  onError
};

export function lexicalJsonToHtml(lexicalState: SerializedEditorState): string {
    setupDomEnvironment()
    const editorNodes = [
      HeadingNode,
      ListNode,
      ListItemNode,
      TableCellNode,
      TableRowNode,
      CustomTableNode,
      {
        replace: TableNode,
        with: () => {
            return new CustomTableNode();
        },
        withKlass: CustomTableNode,
    }] 
    const editor = createHeadlessEditor({ ...initialConfig, nodes: editorNodes });
    const editorState = editor.parseEditorState(lexicalState as SerializedEditorState)
    editor.setEditorState(editorState)
    let html = ''
    
    editor.update(() => {
      html = $generateHtmlFromNodes(editor, null)
    },{discrete:true})

    return html
}


export function lexicalJsonToMarkdown(lexicalState: SerializedEditorState): string {
  const editorNodes = [
    HeadingNode,
    ListNode,
    ListItemNode,
    TableCellNode,
    TableRowNode,
    CustomTableNode,
    {
      replace: TableNode,
      with: () => {
          return new CustomTableNode();
      },
      withKlass: CustomTableNode,
  }] 
  const editor = createHeadlessEditor({ ...initialConfig, nodes: editorNodes });
  const editorState = editor.parseEditorState(lexicalState as SerializedEditorState)
  setupDomEnvironment()

  let markdown = ''

  editor.setEditorState(editorState)

  editor.update(() => {
    markdown = $convertToMarkdownString(TRANSFORMERS)
  },{discrete:true})

  return markdown
}


export function htmlToLexicalJson(html: string): SerializedEditorState {
  setupDomEnvironment()
  const editorNodes = [
    HeadingNode,
    ListNode,
    ListItemNode,
    TableCellNode,
    TableRowNode,
    CustomTableNode,
    {
      replace: TableNode,
      with: () => {
          return new CustomTableNode();
      },
      withKlass: CustomTableNode,
  }] 
  const editor = createHeadlessEditor({ ...initialConfig, nodes: editorNodes });
  editor.update(() => {
    // 使用 jsdom 解析 HTML
    const dom = new JSDOM(html).window.document;
  
    // 生成 LexicalNodes
    const nodes = $generateNodesFromDOM(editor, dom);
  
    // 选择根节点
    $getRoot().select();
  
    // 插入节点
    $insertNodes(nodes);
  },{discrete:true});
  return editor.getEditorState().toJSON()
}

