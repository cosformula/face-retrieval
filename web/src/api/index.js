import request from '@/utils/request'

export const distanceService = {
  get: (params) => request({
    url: `/distances`,
    method: 'get',
    params
  }),
  delete: (id) => request({
    url: `/distances/${id}`,
    method: 'delete'
  }),
  create: (data) => request({
    url: `/distances`,
    method: 'post',
    data
  })
}

export const featureService = {
  get: (params) => request({
    url: `/features`,
    method: 'get',
    params
  }),
  delete: (id) => request({
    url: `/features/${id}`,
    method: 'delete'
  }),
  create: (data) => request({
    url: `/features`,
    method: 'post',
    data
  })
}

export function fetchDistance(distanceID) {
  return request({
    url: `/distances/${distanceID}`,
    method: 'get'
  })
}

export function fetchDistances(libraryID) {
  return request({
    url: '/distances',
    method: 'get',
    params: {
      libraryID
    }
  })
}

export const fetchLibraries = (params) => request({
  url: '/libraries',
  method: 'get',
  params
})

export function fetchLibrary(libraryName) {
  return request({
    url: `/libraries/${libraryName}`,
    method: 'get'
  })
}

export function deleteLibrary(libraryId) {
  return request({
    url: `/libraries/${libraryId}`,
    method: 'delete'
  })
}

export function fetchRetrieval(retrievalID) {
  return request({
    url: `/retrieves/${retrievalID}`
  })
}
export function fetchRetrieves(params) {
  console.log(params)
  return request({
    url: `/retrieves`,
    params
  })
}

export function createRetrieval(libraryID, distanceID, maxIterationFaces, maxIteration, strategy, remark) {
  return request({
    url: `/retrieves`,
    method: 'post',
    data: {
      libraryID,
      distanceID,
      maxIterationFaces,
      maxIteration,
      strategy,
      remark
    }
  })
}

export function createLibrary(data) {
  return request({
    url: `/libraries`,
    method: 'post',
    data
  })
}

export function createIteration(retrievalID, no, answer) {
  return request({
    url: `/retrieves/${retrievalID}/iterations`,
    method: 'post',
    data: {
      no,
      answer
    }
  })
}
export function fetchList(query) {
  return request({
    url: '/article/list',
    method: 'get',
    params: query
  })
}

export function fetchArticle(id) {
  return request({
    url: '/article/detail',
    method: 'get',
    params: {
      id
    }
  })
}

export function fetchPv(pv) {
  return request({
    url: '/article/pv',
    method: 'get',
    params: {
      pv
    }
  })
}

export function createArticle(data) {
  return request({
    url: '/article/create',
    method: 'post',
    data
  })
}

export function updateArticle(data) {
  return request({
    url: '/article/update',
    method: 'post',
    data
  })
}
