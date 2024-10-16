import { Hono } from "hono";
import { userRouter } from "./userRouter";
import { documentsRouter } from "./documentsRouter";
import { insightsRouter } from "./insightsRouter";

const router = new Hono();

router.get("/", (c) =>
  c.text(`
    Hey there, curious wanderer! 🌟
    
    You've stumbled upon the base endpoint of this API. Now, I know what you're thinking: "What kind of magical secrets does this endpoint hold?" Well, brace yourself for the most underwhelming revelation of your life. 

    This endpoint does... absolutely nothing! 🎉
  
    But hey, let's not be too hasty. While you're here, let me entertain you with some fun facts:
    
    1. Did you know that honey never spoils? Archaeologists have found pots of honey in ancient Egyptian tombs that are over 3,000 years old and still perfectly edible. So, if you ever find yourself in a pyramid with a craving for something sweet, you're in luck!
    
    2. The inventor of the frisbee was turned into a frisbee after he died. True story! Fred Morrison, the inventor of the frisbee, was cremated and his ashes were molded into a frisbee. Talk about flying high in the afterlife!
    
    3. If you lift a kangaroo's tail off the ground, it can't hop. Kangaroos use their tails for balance, so without it, they're pretty much stuck. So, if you ever find yourself in a hopping contest with a kangaroo, you know what to do.
    
    But seriously, what are you doing here? This is just the base endpoint. There's a whole world of endpoints out there waiting to be explored. Go forth and conquer, brave adventurer! 🚀
  
    Until next time, stay curious and keep exploring! 🌍
  `)
);

router.route("/user", userRouter);
router.route("/insights", insightsRouter);
router.route("/documents", documentsRouter);

export default router;
