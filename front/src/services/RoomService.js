import http from "../http-common";

export const getAll = () => {
  return http.get("/rooms/");
};

export const get = id => {
  return http.get(`/room/${id}`);
};

export const create = data => {
  return http.post("/rooms/", data);
};

export const update = (id, data) => {
  return http.put(`/rooms/${id}`, data);
};

export const remove = id => {
  return http.delete(`/rooms/${id}`);
};

export const removeAll = () => {
  return http.delete(`/rooms/`);
};

export default {
  getAll,
  get,
  create,
  update,
  remove,
  removeAll
};
