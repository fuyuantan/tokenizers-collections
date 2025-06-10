• Naive Tokenization<br>
• Stemming and Lemmatization<br>
• Byte-Pair Encoding (BPE)<br>
• WordPiece<br>
• SentencePiece and Unigram<br>

一、Naive Tokenization<br>
核心思想：最简单的分词形式是基于空格将文本切分成词元（token）。<br>
局限性：<br>
尽管简单快速，但：<br>
	1. 词汇表问题：<br>
		○ 未登录词 (Out-of-Vocabulary, OOV)：模型的词汇表是在训练数据上构建的。当在实际应用中遇到训练时未见过的词时，模型无法处理，只能将其替换为特殊的“未知”(unknown)词元。<br>
		○ 词形冗余：标点符号、大小写和连字符会导致同一个词被视为不同的词元。例如，world! 和 world 会在词汇表中成为两个独立的词元，增加了词汇表的冗余。<br>
为什么不直接使用其他单位？<br>
	• 按字节 (Byte) 分词：会得到无意义的单个字母，模型难以理解文本含义。<br>
	• 按句子 (Sentence) 分词：句子的数量级远超单词，训练一个理解句子级别输入的模型需要多得多的训练数据。<br>
结论：<br>
单词是比字节或句子更好的基本单位，但并非最优。理想情况下，我们希望将文本分解为最小的有意义单元。例如：<br>
	• 德语中的大量复合词，不适合用空格分割。<br>
	• 英语中的前后缀（如 un- 和 happy 组成 unhappy），本身也携带意义。<br>
因此，我们需要更高级的分词方法。<br>
<br>
二、Stemming and Lemmatization<br>
核心思想：<br>
通过更复杂的算法，将单词的不同变体进行规范化（Normalization），以减少词汇表大小并提高一致性。<br>
主要步骤：<br>
	1. 高级分词：使用正则表达式等工具，将文本精确切分为单词、标点和数字。<br>
	2. 统一大小写：通常将所有文本转换为小写。<br>
	3. 词形归一：<br>
		○ 词干提取 (Stemming)：<br>
			§ 定义：一种更激进的技术，基于规则移除单词的前后缀。<br>
			§ 特点：速度快，但可能会产生无效的单词（非真实词汇）。<br>
			§ 示例：使用 nltk 库的 Porter 词干提取器，"unstably" 会被处理为 "unstabl"。<br>
		○ 词形还原 (Lemmatization)：<br>
			§ 定义：一种更温和的方法，使用词典将单词还原到其基本形式（词元，lemma）。<br>
			§ 特点：几乎总能产生有效的单词。<br>
			§ 示例：使用 nltk 库，"models" 会被还原为 "model"。<br>
局限性：<br>
尽管这些规范化步骤能产出更一致的词汇表，但它们仍然没有解决识别**子词（subword）**等根本性问题。<br>

三、BPE<br>
核心思想：<br>
BPE 是一种自下而上 (bottom-up) 的子词分词算法，通过迭代地合并最高频的相邻字符或词元对来构建词汇表。它最初是一种文本压缩算法，后被 GPT 等模型采用。<br>
工作流程：<br>
	1. 初始化：词汇表从单个字符开始（如英文字母和标点符号）。<br>
	2. 迭代合并：在训练数据中，重复查找最常出现的相邻词元对，并将它们合并成一个新的、更长的子词，加入词汇表中。<br>
	3. 终止：当词汇表达到预设的大小时，停止合并。<br>
主要特点：<br>
	• 处理未知词：BPE 的核心优势在于能将任何未知词分解为其已知的子词单元，从而有效处理 OOV 问题。<br>
	• 预分词器 (Pre-tokenizer)：BPE 本身不定义“单词”的边界，需要一个预分词器（如按空格切分）先将文本分割成初始的单词块。<br>
	• 数据依赖性：BPE 的分词结果完全取决于训练数据，因此需要保存和加载训练好的分词器模型。<br>
	• 空格表示：在 Hugging Face 的实现中，常用特殊字符（如 Ġ）来表示单词间的空格，以区分词首和词中。<br>
	• 应用模型：GPT、BART、RoBERTa 等。<br>

四、WordPiece<br>
核心思想：<br>
WordPiece 是由 Google 提出并用于 BERT 及其变体的一种子词分词算法。它与 BPE 类似，也是自下而上的构建方式。<br>
与 BPE 的主要区别：<br>
	• 合并策略：<br>
		○ BPE：合并频率最高的相邻词元对。<br>
		○ WordPiece：合并能够**最大化训练数据似然（likelihood）**的词元对。<br>
	• 结果差异：由于合并策略不同，WordPiece 倾向于将常见单词保留为单个词元，而 BPE 可能会将常见词也拆分成子词。<br>
主要特点：<br>
	• 子词前缀：使用 ## 前缀来表示一个词元是前一个词元的子词（即非词首部分）。例如，"initialized" 被分为 initial 和 ##ized。<br>
	• BERT 中的特定设计：<br>
		○ BERT 的 WordPiece 分词器会自动处理文本转小写。<br>
		○ 会自动添加 [CLS]（句首）和 [SEP]（句末）等特殊标记。这些并非 WordPiece 算法本身的要求。<br>

五、SentencePiece and Unigram<br>
Unigram 算法<br>
核心思想：<br>
Unigram 是一种自上而下 (top-down) 的分词算法。<br>
工作流程：<br>
	1. 初始化：从一个包含所有词和大量可能子词的庞大词汇表开始。<br>
	2. 迭代修剪：根据一个对数似然分数 (log-likelihood score)，逐步从词汇表中移除“价值”最低的词元，直到词汇表达到目标大小。<br>
主要特点：<br>
	• 统计性：训练好的 Unigram 分词器是统计性的，而非基于固定规则。它为每个词元保存了概率，用于在分词时选择最优的分割方式。<br>
SentencePiece<br>
核心思想：<br>
SentencePiece 是一个集成的分词工具，它将输入文本视为原始的 Unicode 字符流，无需预分词。这使其成为一种与语言无关的分词解决方案。<br>
主要特点：<br>
	• 多语言友好：对于像中文这样不使用空格分隔单词的语言，SentencePiece 尤其有用。<br>
	• 集成算法：它内部可以使用 BPE 或 Unigram 算法来完成最终的分词任务。<br>
	• 空格处理：它通过在词首添加特殊字符（如下划线_）来编码空格，从而在解码时恢复原文。<br>
	• 独立性：可以作为独立的库（如 Google 的 sentencepiece）使用，也可以集成在 Hugging Face 等框架中。<br>

1-5 output results:

![1](https://github.com/user-attachments/assets/66517bec-5c60-4d9e-a29e-7981b0b63b6d)

![2](https://github.com/user-attachments/assets/08156b2d-071d-4733-854e-b40f6330aedf)

![3](https://github.com/user-attachments/assets/c10353e1-6a77-4d1d-b9c8-aceffe2f4dc7)

![4](https://github.com/user-attachments/assets/4c83ccb4-1fcd-4489-8731-d62a118c402c)

![5](https://github.com/user-attachments/assets/6997f8d1-0597-4c52-8e36-8ec7579e30af)




