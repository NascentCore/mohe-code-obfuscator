import { SerializedEditorState } from "lexical";


export interface DocumentCreateRequest {
    title: string;
    state?: SerializedEditorState;
    extra?: Record<string, any>;
}

export interface DocumentUpdateRequest {
    title?: string;
    state?: SerializedEditorState;
    extra?: Record<string, any>;
}

export interface DocumentListRequest {
    page?: number;
    page_size?: number;
    order_by?: 'created_at' | 'updated_at' | 'title';
    order?: 'asc' | 'desc';
}

export interface DocumentListResponse {
    total: number;
    pages: number;
    page: number;
    page_size: number;
    items: Document[];
} 