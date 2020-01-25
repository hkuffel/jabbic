var trace1 = {
    labels: ['Calendars', 'Comics & Graphic Novels', 'Test Preparation',
    'Mystery, Thriller & Suspense', 'Science Fiction & Fantasy',
    'Romance', 'Humor & Entertainment', 'Literature & Fiction',
    'Gay & Lesbian', 'Engineering & Transportation',
    'Cookbooks, Food & Wine', 'Crafts, Hobbies & Home',
    'Arts & Photography', 'Education & Teaching',
    'Parenting & Relationships', 'Self-Help', 'Computers & Technology',
    'Medical Books', 'Science & Math', 'Health, Fitness & Dieting',
    'Business & Money', 'Law', 'Biographies & Memoirs', 'History',
    'Politics & Social Sciences', 'Reference',
    'Christian Books & Bibles', 'Religion & Spirituality',
    'Sports & Outdoors', 'Teen & Young Adult', "Children's Books",
    'Travel'],
    values: [6460,
        4261,
        9965,
        2636,
        13605,
        9139,
        3026,
        7979,
        8802,
        9934,
        1664,
        2672,
        1339,
        11886,
        6807,
        6896,
        7314,
        7580,
        12086,
        1998,
        2523,
        3402,
        3268,
        7559,
        4291,
        9276,
        3800,
        2703,
        5968,
        7489,
        2906,
        18338],
    type: 'pie'
  };
  
  var data = [trace1];
  
  var layout = {
    title: "Book Genre Distribution",
  };
  
  Plotly.newPlot("plot", data, layout);  