import instaloader


ig = instaloader.Instaloader()

insta_page = "nna.n3582"
ig.login("platinum.cats", "Cats_platinum2023")
ig.download_profile(insta_page, profile_pic_only=False)
