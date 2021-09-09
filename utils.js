const randomColor = (type = 'hex') => {
  // 生成随机颜色

  let red = Math.floor(Math.random() * 256);
  let green = Math.floor(Math.random() * 256);
  let blue = Math.floor(Math.random() * 256);

  let colors = '#00FF00';

  switch (type) {
    case "hex":
      colors = '#' + red.toString(16) + green.toString(16) + blue.toString(16);
      break;
    case "rgb":
      colors = '(' + red + ',' + green + ',' + blue + ')';
      break;
  }

  return colors
};

const hexToRgb = (color) => {
  color = color.toLowerCase();
  let reg = /^#([0-9a-fA-f]{3}|[0-9a-fA-f]{6})$/;

  if (color && reg.test(color)) {
    if (color.length === 4) {
      let colorNew = "#";

      for (let i = 1; i < 4; i += 1) {
        colorNew += color.slice(i, i + 1).concat(color.slice(i, i + 1));
      }
      color = colorNew;
    }
    //处理六位的颜色值
    let colorChange = [];
    for (let i = 1; i < 7; i += 2) {
      colorChange.push(parseInt("0x" + color.slice(i, i + 2)));
    }
    return "(" + colorChange.join(",") + ")";
  }

  return color
};

const gradualChangeColor = (color, level = 0.5, type = 'light') => {
  // 得到rgb颜色值为color的减淡颜色值，level为加深的程度，限0-1之间
  let newColor = 'rgb(';

  color = color.substring(1, color.length);  // 删除rgb颜色字符串的第一个'('
  color = color.substring(0, color.length - 1);  // 删除rgb颜色字符串的最后一个')'
  color = color.split(',');

  for (let i = 0; i < 3; i++) {
    let value = parseInt(color[i].replace(/\s*/g, ""));
    if (type === 'light') {
      newColor += Math.floor((255 - value) * level + value);
    } else if (type === 'dark') {
      newColor += Math.floor(color[i] * (1 - level));
    } else {
      return new Error("未知的颜色渐变类型！");
    }

    if (i < 2) {
      newColor += ',';
    }
  }

  newColor += ')';

  return newColor;
};

const randomInt = (range = 10) => {
  // 生成随机数

  let number = Math.random() * range;

  return Math.floor(number)
};


export default {
  randomColor,
  randomInt,
  gradualChangeColor,
  hexToRgb,
};
