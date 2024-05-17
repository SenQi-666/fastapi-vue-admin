export interface searchDataType {
  request_path?: string;
  creator?: number;
  creator_name?: string;
  date_range?: [string, string];
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

export interface searchCreatorDataType {
  name?: string;
  available?: string;
}

export interface creatorTableDataType {
  id?: number;
  name?: string;
  available?: string;
  description?: string;
}