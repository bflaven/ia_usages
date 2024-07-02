# vite_vue_prompt_18.md


## prompt

Generate a JSON sample of 10 notes with real value for "title", "content", "category", "published" either true or false, "createdAt", "updatedAt" with random value in the same time format. Do use the json model given below :

```js
{
  "title": "string",
  "content": "string",
  "category": "string",
  "published": false,
  "createdAt": "2024-06-29T11:24:39.688Z",
  "updatedAt": "2024-06-29T11:24:39.688Z"
}
```


## Mistral
Sure, here is a JSON sample of 10 notes with real values:

```js
[
  {
    "title": "Note 1",
    "content": "This is the content of note 1",
    "category": "Personal",
    "published": true,
    "createdAt": "2022-01-01T00:00:00.000Z",
    "updatedAt": "2022-01-01T00:00:00.000Z"
  },
  {
    "title": "Note 2",
    "content": "This is the content of note 2",
    "category": "Work",
    "published": false,
    "createdAt": "2022-01-02T00:00:00.000Z",
    "updatedAt": "2022-01-02T00:00:00.000Z"
  },
  {
    "title": "Note 3",
    "content": "This is the content of note 3",
    "category": "Personal",
    "published": true,
    "createdAt": "2022-01-03T00:00:00.000Z",
    "updatedAt": "2022-01-03T00:00:00.000Z"
  },
  {
    "title": "Note 4",
    "content": "This is the content of note 4",
    "category": "Work",
    "published": false,
    "createdAt": "2022-01-04T00:00:00.000Z",
    "updatedAt": "2022-01-04T00:00:00.000Z"
  },
  {
    "title": "Note 5",
    "content": "This is the content of note 5",
    "category": "Personal",
    "published": true,
    "createdAt": "2022-01-05T00:00:00.000Z",
    "updatedAt": "2022-01-05T00:00:00.000Z"
  },
  {
    "title": "Note 6",
    "content": "This is the content of note 6",
    "category": "Work",
    "published": false,
    "createdAt": "2022-01-06T00:00:00.000Z",
    "updatedAt": "2022-01-06T00:00:00.000Z"
  },
  {
    "title": "Note 7",
    "content": "This is the content of note 7",
    "category": "Personal",
    "published": true,
    "createdAt": "2022-01-07T00:00:00.000Z",
    "updatedAt": "2022-01-07T00:00:00.000Z"
  },
  {
    "title": "Note 8",
    "content": "This is the content of note 8",
    "category": "Work",
    "published": false,
    "createdAt": "2022-01-08T00:00:00.000Z",
    "updatedAt": "2022-01-08T00:00:00.000Z"
  },
  {
    "title": "Note 9",
    "content": "This is the content of note 9",
    "category": "Personal",
    "published": true,
    "createdAt": "2022-01-09T00:00:00.000Z",
    "updatedAt": "2022-01-09T00:00:00.000Z"
  },
  {
    "title": "Note 10",
    "content": "This is the content of note 10",
    "category": "Work",
    "published": false,
    "createdAt": "2022-01-10T00:00:00.000Z",
    "updatedAt": "2022-01-10T00:00:00.000Z"
  }
]
```