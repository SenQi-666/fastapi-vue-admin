export interface searchDataType {
  username?: string
  name?: string
  available?: string
}

export interface searchSelectDataType {
  name?: string
  available?: string
}

export interface tableDataType {
  id?: number;
  index?: number;
  username?: string;
  name?: string;
  email?: string;
  mobile?: string;
  gender?: number;
  password?: string;
  dept_id: deptTreeType['id'];
  dept_name?: deptTreeType['name'];
  roles?: roleSelectorType[];
  roleNames?: string;
  role_ids?: roleSelectorType['id'][];
  positions?: positionSelectorType[];
  positionNames?: string;
  position_ids?: positionSelectorType['id'][];
  is_superuser?: boolean;
  available?: boolean;
  description?: string;
  last_login?: string;
  created_at?: string;
  updated_at?: string;
  creator?: creatorType;
  creatorName?: creatorType['name'];
}

export interface deptTreeType {
  id?: number;
  name?: string;
  parent_id?: number;
  children?: deptTreeType[];
}

export interface roleSelectorType {
  id?: number;
  name?: string;
  available?: boolean;
  description?: string;
}

export interface positionSelectorType {
  id?: number;
  name?: string;
  available?: boolean;
  description?: string;
}

interface creatorType {
  id?: number;
  name?: string;
}