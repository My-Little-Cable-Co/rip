RIPPING_GUIDE_SCHEMA = {
  "$schema": "http://json-schema.org/draft-07/schema#", 
  "$id": "https://mylittlecable.co/rip/ripping-guide-schema.json", 
  "title": "Root", 
  "type": "object",
  "required": [
    "disc_id",
    "title"
  ],
  "properties": {
    "disc_id": {
      "$id": "#root/disc_id", 
      "title": "Disc_id", 
      "type": "string",
      "default": "",
      "examples": [
        "2fd061ade372087da9ac72b6c804d4fe"
      ],
      "pattern": "^[0-9a-f]{32}$"
    },
    "title": {
      "$id": "#root/title", 
      "title": "Title", 
      "type": "string",
      "default": "",
      "examples": [
        "Big Buck Bunny"
      ],
      "pattern": "^.*$"
    },
    "episodes": {
      "$id": "#root/episodes", 
      "title": "Episodes", 
      "type": "array",
      "default": [],
      "items":{
        "$id": "#root/episodes/items", 
        "title": "Items", 
        "type": "object",
        "required": [
          "show_title",
          "season",
          "episode",
          "filename",
          "title",
          "chapters"
        ],
        "properties": {
          "show_title": {
            "$id": "#root/episodes/items/show_title", 
            "title": "Show title", 
            "type": "string",
            "default": "",
            "examples": [
              "Big Buck Bunny the Animated Series"
            ],
            "pattern": "^.*$"
          },
          "season": {
            "$id": "#root/episodes/items/season", 
            "title": "Season", 
            "type": "string",
            "default": "",
            "examples": [
              "01"
            ],
            "pattern": "^.*$"
          },
          "episode": {
            "$id": "#root/episodes/items/episode", 
            "title": "Episode", 
            "type": "string",
            "default": "",
            "examples": [
              "17"
            ],
            "pattern": "^.*$"
          },
          "filename": {
            "$id": "#root/episodes/items/filename", 
            "title": "Filename", 
            "type": "string",
            "default": "",
            "examples": [
              "Big Buck Bunny.S01.E17.m4v"
            ],
            "pattern": "^.*$"
          },
          "title": {
            "$id": "#root/episodes/items/title", 
            "title": "Title", 
            "type": "string",
            "default": "",
            "examples": [
              "1"
            ],
            "pattern": "^[0-9]+$"
          },
          "chapters": {
            "$id": "#root/episodes/items/chapters", 
            "title": "Chapters", 
            "type": "string",
            "default": "",
            "examples": [
              "1-6"
            ],
            "pattern": "^[0-9]+(-[0-9]+)?$"
          }
        }
      }
    },
    "features": {
      "$id": "#root/features", 
      "title": "Features", 
      "type": "array",
      "default": [],
      "items":{
        "$id": "#root/features/items", 
        "title": "Items", 
        "type": "object",
        "required": [
          "feature_title",
          "filename",
          "title",
          "chapters"
        ],
        "properties": {
          "feature_title": {
            "$id": "#root/features/items/feature_title", 
            "title": "Feature_title", 
            "type": "string",
            "default": "",
            "examples": [
              "Big Buck Bunny the Motion Picture"
            ],
            "pattern": "^.*$"
          },
          "filename": {
            "$id": "#root/features/items/filename", 
            "title": "Filename", 
            "type": "string",
            "default": "",
            "examples": [
              "Big Buck Bunny the Motion Picture.m4v"
            ],
            "pattern": "^.*$"
          },
          "title": {
            "$id": "#root/features/items/title", 
            "title": "Title", 
            "type": "string",
            "default": "",
            "examples": [
              "1"
            ],
            "pattern": "^[0-9]+$"
          },
          "chapters": {
            "$id": "#root/features/items/chapters", 
            "title": "Chapters", 
            "type": "string",
            "default": "",
            "examples": [
              "1-20"
            ],
            "pattern": "^[0-9]+(-[0-9]+)?$"
          },
          "special_features": {
            "$id": "#root/features/items/special_features", 
            "title": "Special_features", 
            "type": "array",
            "default": [],
            "items":{
              "$id": "#root/features/items/special_features/items", 
              "title": "Items", 
              "type": "object",
              "required": [
                "special_feature_title",
                "filename",
                "title",
                "chapters"
              ],
              "properties": {
                "special_feature_title": {
                  "$id": "#root/features/items/special_features/items/special_feature_title", 
                  "title": "Special_feature_title", 
                  "type": "string",
                  "default": "",
                  "examples": [
                    "Buck Gets His Revenge"
                  ],
                  "pattern": "^.*$"
                },
                "filename": {
                  "$id": "#root/features/items/special_features/items/filename", 
                  "title": "Filename", 
                  "type": "string",
                  "default": "",
                  "examples": [
                    "Buck Gets His Revenge-deleted.m4v"
                  ],
                  "pattern": "^.*$"
                },
                "title": {
                  "$id": "#root/features/items/special_features/items/title", 
                  "title": "Title", 
                  "type": "string",
                  "default": "",
                  "examples": [
                    "40"
                  ],
                  "pattern": "^[0-9]+$"
                },
                "chapters": {
                  "$id": "#root/features/items/special_features/items/chapters", 
                  "title": "Chapters", 
                  "type": "string",
                  "default": "",
                  "examples": [
                    "1"
                  ],
                  "pattern": "^[0-9]+(-[0-9]+)?$"
                }
              }
            }
          }
        }
      }
    }
  }
}
