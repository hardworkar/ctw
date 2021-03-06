# yep arithmetic coding
# https://www.cbloom.com/algs/statisti.html#A1.0

class Coder():
  def __init__(self, ob = []):
    self.PRECISION = 32 
    self.SHIFT = self.PRECISION - 1
    self.MAX_VALUE = (1 << self.PRECISION) - 1 # [1] * PRECISION

    self.low = 0
    self.high =  self.MAX_VALUE
    self.ob = ob
    self.pending = 0

  def getCoded(self):
    # after all, don't forget to send the rest of low or high:
    # low:  0b01..1
    # high: 0b10..0
    assert (self.high >> self.SHIFT) == 1
    return self.ob + [self.high >> self.SHIFT] + [0] * (self.PRECISION - 1)

  # should produce < (-math.log2(p_x) + 2) bits...    
  # probably make p_0 rational
  def code(self, p_0, x = None):

    assert self.low < self.high 
    assert self.low  >= 0 and self.low  <= self.MAX_VALUE
    assert self.high >= 0 and self.high <= self.MAX_VALUE

    decode = (x == None)
    
    # [0, p_0) or [p_0, 1)
    split = self.low + int(((self.high - self.low) * p_0))

    if decode:
      if len(self.ob) < self.PRECISION:
        raise StopIteration
      zomb = 0
      for i in range (self.PRECISION):
        zomb <<= 1
        zomb |= self.ob[i] 
      x = int(zomb >= split)

    if x == 0:
      self.high = split
    elif x == 1:
      self.low = split
    

    # what if we have more input, but can't throw out any bits??
    # bits that will never change
    while ((self.low >> self.SHIFT) == (self.high >> self.SHIFT)):
      if decode:
        assert self.ob[0] == (self.low >> self.SHIFT)
        assert len(self.ob) > 0
        self.ob = self.ob[1:]
      else:
        assert (self.low >> self.SHIFT) <= 1
        bit = self.low >> self.SHIFT
        self.ob.append(bit)
      # get rid of MSB, then shift
      # (1 << SHIFT) - 1 == [1] * SHIFT 
      self.low =   (self.low  & ((1 << self.SHIFT) - 1)) << 1
      self.high = ((self.high & ((1 << self.SHIFT) - 1)) << 1) | 1

    return x
