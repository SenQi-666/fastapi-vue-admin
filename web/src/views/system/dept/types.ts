export interface treeDataType {
  id?: number;
  name?: string;
  order?: number;
  parent_id?: number;
  available?: boolean;
  description?: string;
  children?: treeDataType[];
}
