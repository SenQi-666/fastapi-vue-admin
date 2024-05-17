export interface searchDataType {
  name?: string
  available?: string
}

export interface tableDataType {
  id?: number;
  index?: number;
  name?: string;
  order?: number;
  available?: boolean;
  description?: string;
  created_at?: string;
  updated_at?: string;
}