export interface tableDataType {
  id?: number;
  name?: string;
  type?: number;
  icon?: string;
  order?: number;
  permission?: string;
  route_name?: string;
  route_path?: string;
  component_path?: string;
  redirect?: string;
  parent_id?: number;
  parent_name?: string;
  cache?: boolean;
  hidden?: boolean;
  available?: boolean;
  description?: string;
  created_at?: string;
  updated_at?: string;
  children?: tableDataType[];
}